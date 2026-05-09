"""Incident management commands."""

from datetime import datetime, timedelta, timezone
import json
import re
import warnings

import click
import requests
from rich.console import Console
from rich.table import Table
from puppy_kit.client import get_datadog_client
from puppy_kit.config import load_config
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.confirm import confirm_action
from puppy_kit.utils.format import json_list_response

warnings.filterwarnings("ignore", message=".*is unstable.*")

console = Console()

SEVERITY_CHOICES = ["SEV-1", "SEV-2", "SEV-3", "SEV-4", "SEV-5"]
STATUS_CHOICES = ["active", "stable", "resolved"]


def _stringify_enum(value, default="unknown"):
    """Convert SDK enum values to strings for CLI output."""
    return str(value) if value else default


def _stringify_datetime(value, default="unknown"):
    """Convert datetime-like values to strings for CLI output."""
    return str(value) if value else default


def _impact_label(value):
    """Render customer impact consistently in table output."""
    if value is True:
        return "[bold red]Impacted[/bold red]"
    if value is False:
        return "[dim]No[/dim]"
    return "[dim]unknown[/dim]"


def _get_attr(attrs, field, default=""):
    """Safely get attribute, checking _data_store if needed."""
    val = getattr(attrs, field, None)
    data_store = getattr(attrs, "_data_store", None)
    if val is None and isinstance(data_store, dict):
        val = data_store.get(field, None)
    return default if val is None else val


def _get_incident_field_value(attrs, field_key):
    """Read an incident custom field value from attributes.fields."""
    fields = _get_attr(attrs, "fields", None)
    if isinstance(fields, dict):
        field_obj = fields.get(field_key)
        if isinstance(field_obj, dict):
            return field_obj.get("value", None)
        return getattr(field_obj, "value", None)
    return None


def _incident_state(attrs):
    """Extract incident state with fallback to custom fields payload."""
    return _get_attr(attrs, "state", _get_incident_field_value(attrs, "state"))


def _incident_severity(attrs):
    """Extract incident severity with fallback to custom fields payload."""
    return _get_attr(attrs, "severity", _get_incident_field_value(attrs, "severity"))


@click.group()
def incident():
    """Incident management commands."""
    pass


@incident.command(name="list")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@click.option(
    "--status",
    type=click.Choice(["active", "stable", "resolved"]),
    default=None,
    help="Convenience filter mapped to a state:<value> search query fragment",
)
@click.option(
    "--limit", "page_size", type=int, default=100, help="Max incidents to return [default: 100]"
)
@click.option("--query", default="", help="Datadog incident search query using facet syntax")
@click.option(
    "--sort",
    type=click.Choice(["created", "-created"]),
    default="-created",
    help="Sort incidents by creation time",
)
@click.option(
    "--since",
    default=None,
    help="Only include incidents newer than this cutoff (for example: '14 days', '24 hours', '2026-02-25')",
)
@handle_api_error
def list_incidents(
    format: str, status: str | None, page_size: int, query: str, sort: str, since: str | None
) -> None:
    """List incidents with Datadog search queries, sorting, and optional cutoff pagination."""
    from typing import Any, cast
    from datadog_api_client.v2.model.incident_search_sort_order import IncidentSearchSortOrder  # noqa: F401

    def _parse_since(value: str | None) -> datetime | None:
        if value is None:
            return None

        normalized = value.strip()
        if not normalized:
            raise click.UsageError(
                "Invalid --since value: expected 'N days', 'N hours', or YYYY-MM-DD."
            )

        relative_match = re.fullmatch(r"(?i)(\d+)\s+(day|days|hour|hours)", normalized)
        if relative_match:
            amount = int(relative_match.group(1))
            unit = relative_match.group(2).lower()
            now = datetime.now(timezone.utc)
            if "day" in unit:
                return now - timedelta(days=amount)
            return now - timedelta(hours=amount)

        try:
            parsed_date = datetime.strptime(normalized, "%Y-%m-%d")
        except ValueError as exc:
            raise click.UsageError(
                f"Invalid --since value '{value}': expected 'N days', 'N hours', or YYYY-MM-DD."
            ) from exc

        return parsed_date.replace(tzinfo=timezone.utc)

    def _coerce_utc_datetime(value: object) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return (
                value.replace(tzinfo=timezone.utc)
                if value.tzinfo is None
                else value.astimezone(timezone.utc)
            )
        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                return None
            if normalized.endswith("Z"):
                normalized = f"{normalized[:-1]}+00:00"
            try:
                parsed = datetime.fromisoformat(normalized)
            except ValueError:
                return None
            return (
                parsed.replace(tzinfo=timezone.utc)
                if parsed.tzinfo is None
                else parsed.astimezone(timezone.utc)
            )
        return None

    cutoff = _parse_since(since)
    if cutoff is not None and sort != "-created":
        raise click.UsageError("--since requires --sort=-created so pagination can stop early.")

    client = get_datadog_client()

    all_incidents: list[object] = []
    page_offset: int | None = 0
    effective_page_size = min(page_size, 100)

    query_parts: list[str] = []
    if query.strip():
        query_parts.append(query.strip())
    if status:
        query_parts.append(f"state:{status}")
    search_query = " ".join(query_parts)

    with console.status("[cyan]Fetching incidents...[/cyan]"):
        while page_offset is not None:
            response = client.incidents.search_incidents(
                search_query,
                sort=cast(Any, sort),  # SDK accepts str at runtime
                page_size=effective_page_size,
                page_offset=page_offset,
            )

            response_data = getattr(response, "data", None)
            response_attrs = getattr(response_data, "attributes", None)
            search_results = list(getattr(response_attrs, "incidents", []) or [])
            incidents = [getattr(result, "data", result) for result in search_results]
            if not incidents:
                break

            if cutoff is not None:
                filtered_page = []
                for inc in incidents:
                    attrs = getattr(inc, "attributes", None)
                    created_at = _coerce_utc_datetime(_get_attr(attrs, "created", None))
                    if created_at is not None and created_at >= cutoff:
                        filtered_page.append(inc)
                all_incidents.extend(filtered_page)
                if len(all_incidents) >= page_size:
                    break

                last_incident = incidents[-1]
                last_attrs = getattr(last_incident, "attributes", None)
                last_created = _coerce_utc_datetime(_get_attr(last_attrs, "created", None))
                if last_created is not None and last_created < cutoff:
                    break
            else:
                all_incidents.extend(incidents)
                if len(all_incidents) >= page_size:
                    break

            pagination = getattr(getattr(response, "meta", None), "pagination", None)
            next_offset = getattr(pagination, "next_offset", None)
            if next_offset is None:
                next_offset = getattr(response_attrs, "next_offset", None)
            if next_offset is None:
                break

            page_offset = int(next_offset)

    all_incidents = all_incidents[:page_size]

    if format == "json":
        output = []
        for inc in all_incidents:
            attrs = getattr(inc, "attributes", None)
            output.append(
                {
                    "id": _get_attr(inc, "id", ""),
                    "title": _get_attr(attrs, "title", ""),
                    "severity": _stringify_enum(_incident_severity(attrs), "unknown"),
                    "status": _stringify_enum(_incident_state(attrs), "unknown"),
                    "customer_impacted": _get_attr(attrs, "customer_impacted", "unknown"),
                    "public_id": _get_attr(inc, "public_id", "unknown"),
                    "detected": _stringify_datetime(_get_attr(attrs, "detected", "")),
                    "resolved": _stringify_datetime(_get_attr(attrs, "resolved", "")),
                    "created": _stringify_datetime(_get_attr(attrs, "created", "")),
                    "modified": _stringify_datetime(_get_attr(attrs, "modified", "")),
                }
            )
        click.echo(json.dumps(json_list_response(output)))
    else:
        table = Table(title="Incidents")
        table.add_column("ID", style="cyan", width=36)
        table.add_column("Title", style="white", min_width=30)
        table.add_column("Severity", style="yellow", width=10)
        table.add_column("Status", style="bold", width=12)
        table.add_column("Description", style="white", width=12)
        table.add_column("Created", style="dim", width=20)

        for inc in all_incidents:
            attrs = getattr(inc, "attributes", None)
            status_str = _stringify_enum(_incident_state(attrs), "unknown")
            severity_str = _stringify_enum(_incident_severity(attrs), "unknown")
            status_color = {
                "active": "red",
                "stable": "yellow",
                "resolved": "green",
            }.get(status_str, "white")

            table.add_row(
                str(_get_attr(inc, "id", "")),
                str(_get_attr(attrs, "title", "")),
                severity_str,
                f"[{status_color}]{status_str}[/{status_color}]",
                _impact_label(_get_attr(attrs, "customer_impacted", "unknown")),
                _stringify_datetime(_get_attr(attrs, "created", "")),
            )

        console.print(table)
        console.print(f"\n[dim]Total incidents: {len(all_incidents)}[/dim]")


TIMELINE_CELL_LIMIT = 10


def _fetch_custom_fields(incident_id: str, config) -> dict:
    """Fetch custom field values for an incident. Returns a flat key→value dict."""
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
    }
    url = f"https://api.{config.site}/api/v2/incidents/{incident_id}"
    try:
        resp = requests.get(
            url, headers=headers, params={"include": "user_defined_fields"}, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {}

    fields_obj = data.get("data", {}).get("attributes", {}).get("fields", {})
    result = {}
    if isinstance(fields_obj, dict):
        for key, value_obj in fields_obj.items():
            if isinstance(value_obj, dict):
                field_value = value_obj.get("value")
            else:
                field_value = getattr(value_obj, "value", None)
            if field_value is not None:
                result[key] = field_value
    return result


def _fetch_timeline_cells(incident_id: str, config) -> tuple[list[dict], bool]:
    """Fetch timeline cells for an incident. Returns (cells, truncated)."""
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
    }
    url = f"https://api.{config.site}/api/v2/incidents/{incident_id}/timeline"
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        all_cells = resp.json().get("data", [])
    except Exception:
        return [], False

    truncated = len(all_cells) > TIMELINE_CELL_LIMIT
    cells = all_cells[:TIMELINE_CELL_LIMIT]
    output = []
    for cell in cells:
        cell_attrs = cell.get("attributes", {})
        output.append(
            {
                "id": cell.get("id", ""),
                "cell_type": cell_attrs.get("cell_type", ""),
                "created": cell_attrs.get("created", ""),
                "content": cell_attrs.get("content", {}),
            }
        )
    return output, truncated


@incident.command(name="get")
@click.argument("incident_id")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def get_incident(incident_id, format):
    """Get incident details including custom fields and timeline cells."""
    client = get_datadog_client()
    config = load_config()

    with console.status(f"[cyan]Fetching incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
        custom_fields = _fetch_custom_fields(incident_id, config)
        timeline_cells, truncated = _fetch_timeline_cells(incident_id, config)

    inc = response.data
    attrs = inc.attributes

    if format == "json":
        output = {
            "id": inc.id,
            "title": getattr(attrs, "title", ""),
            "severity": _stringify_enum(_incident_severity(attrs), "unknown"),
            "status": _stringify_enum(_incident_state(attrs), "unknown"),
            "customer_impacted": getattr(attrs, "customer_impacted", "unknown"),
            "public_id": getattr(inc, "public_id", "unknown"),
            "detected": _stringify_datetime(getattr(attrs, "detected", "")),
            "resolved": _stringify_datetime(getattr(attrs, "resolved", "")),
            "created": _stringify_datetime(getattr(attrs, "created", "")),
            "modified": _stringify_datetime(getattr(attrs, "modified", "")),
            "fields": custom_fields,
            "timeline": timeline_cells,
        }
        if truncated:
            output["timeline_truncated"] = True
            output["timeline_hint"] = (
                f"Timeline truncated to {TIMELINE_CELL_LIMIT} cells. "
                "Use dd_incidents_get_timeline for the full output."
            )
        click.echo(json.dumps(output))
    else:
        console.print(f"\n[bold cyan]Incident {inc.id}[/bold cyan]")
        console.print(f"[bold]Title:[/bold] {getattr(attrs, 'title', '')}")

        severity_str = _stringify_enum(_incident_severity(attrs), "unknown")
        console.print(f"[bold]Severity:[/bold] [yellow]{severity_str}[/yellow]")

        status_str = _stringify_enum(_incident_state(attrs), "unknown")
        status_color = {
            "active": "red",
            "stable": "yellow",
            "resolved": "green",
        }.get(status_str, "white")
        console.print(f"[bold]Status:[/bold] [{status_color}]{status_str}[/{status_color}]")

        console.print(f"[bold]Description:[/bold] {getattr(attrs, 'customer_impacted', 'unknown')}")
        console.print(f"[bold]Public ID:[/bold] {getattr(inc, 'public_id', 'unknown')}")
        console.print(
            f"[bold]Detected:[/bold] {_stringify_datetime(getattr(attrs, 'detected', ''))}"
        )
        console.print(
            f"[bold]Resolved:[/bold] {_stringify_datetime(getattr(attrs, 'resolved', ''))}"
        )
        console.print(f"[bold]Created:[/bold] {_stringify_datetime(getattr(attrs, 'created', ''))}")
        console.print(
            f"[bold]Modified:[/bold] {_stringify_datetime(getattr(attrs, 'modified', ''))}"
        )

        if custom_fields:
            console.print("\n[bold]Fields[/bold]")
            for key, value in sorted(custom_fields.items()):
                console.print(f"  [cyan]{key}:[/cyan] {value}")

        if timeline_cells:
            console.print(f"\n[bold]Timeline[/bold] [dim]({len(timeline_cells)} cells)[/dim]")
            for cell in timeline_cells:
                cell_type = cell.get("cell_type", "")
                created = cell.get("created", "")[:19]
                content = cell.get("content", {})
                console.print(f"\n  [dim]{created}[/dim] [yellow]{cell_type}[/yellow]")
                if cell_type == "markdown":
                    console.print(f"  {content.get('content', '')[:500]}")
                elif cell_type == "incident_status_change":
                    action = content.get("action", "")
                    after = content.get("after", {})
                    before = content.get("before", {})
                    if action == "created":
                        console.print(
                            f"  Created — {after.get('title', '')} {after.get('severity', '')}"
                        )
                    elif action == "updated":
                        for key in set(list(before.keys()) + list(after.keys())):
                            if before.get(key) != after.get(key):
                                console.print(
                                    f"  {key}: {before.get(key, '')} → {after.get(key, '')}"
                                )
                else:
                    console.print(f"  {json.dumps(content)[:200]}")
            if truncated:
                console.print(
                    f"\n  [dim]Timeline truncated to {TIMELINE_CELL_LIMIT} cells. "
                    "Use `puppy incident timeline list` for the full output.[/dim]"
                )


@incident.command(name="create")
@click.option("--title", required=True, help="Incident title")
@click.option(
    "--severity",
    type=click.Choice(SEVERITY_CHOICES),
    required=False,
    default=None,
    help="Incident severity",
)
@click.option("--team", default=None, help="Team name for the 'teams' autocomplete field")
@click.option("--assignee", default=None, help="Assignee user ID (UUID) to set as commander")
@click.option(
    "--customer-impacted",
    "customer_impacted",
    is_flag=True,
    default=False,
    help="Set if customers are experiencing impact",
)
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def create_incident(title, severity, team, assignee, customer_impacted, format):
    """Create a new incident."""
    from datadog_api_client.v2.model.incident_create_request import IncidentCreateRequest
    from datadog_api_client.v2.model.incident_create_data import IncidentCreateData
    from datadog_api_client.v2.model.incident_create_attributes import IncidentCreateAttributes
    from datadog_api_client.v2.model.incident_create_relationships import (
        IncidentCreateRelationships,
    )
    from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser
    from datadog_api_client.v2.model.nullable_relationship_to_user_data import (
        NullableRelationshipToUserData,
    )
    from datadog_api_client.v2.model.users_type import UsersType
    from datadog_api_client.v2.model.incident_type import IncidentType

    client = get_datadog_client()

    from typing import Any

    fields_dict: dict[str, Any] = {}
    if severity is not None:
        fields_dict["severity"] = {"type": "dropdown", "value": severity}
    if team is not None:
        fields_dict["teams"] = {"type": "autocomplete", "value": [team]}

    relationships = None
    if assignee:
        relationships = IncidentCreateRelationships(
            commander_user=NullableRelationshipToUser(
                data=NullableRelationshipToUserData(type=UsersType("users"), id=assignee)
            )
        )

    data_kwargs: dict[str, Any] = dict(
        type=IncidentType("incidents"),
        attributes=IncidentCreateAttributes(
            title=title,
            customer_impacted=customer_impacted,
            fields=fields_dict,
        ),
    )
    if relationships is not None:
        data_kwargs["relationships"] = relationships

    body = IncidentCreateRequest(data=IncidentCreateData(**data_kwargs))

    with console.status("[cyan]Creating incident...[/cyan]"):
        response = client.incidents.create_incident(body=body)

    inc = response.data
    attrs = inc.attributes

    if format == "json":
        output = {
            "id": inc.id,
            "title": getattr(attrs, "title", ""),
            "severity": _stringify_enum(_incident_severity(attrs), severity or "unknown"),
            "status": _stringify_enum(_incident_state(attrs), "unknown"),
        }
        click.echo(json.dumps(output))
    else:
        console.print(f"[green]Incident {inc.id} created[/green]")
        console.print(f"[bold]Title:[/bold] {getattr(attrs, 'title', '')}")
        console.print(
            f"[bold]Severity:[/bold] {_stringify_enum(_incident_severity(attrs), severity or 'unknown')}"
        )
        console.print(f"[bold]Status:[/bold] {_stringify_enum(_incident_state(attrs), 'unknown')}")


@incident.command(name="update")
@click.argument("incident_id")
@click.option("--title", default=None, help="New incident title")
@click.option("--status", default=None, type=click.Choice(STATUS_CHOICES), help="Incident status")
@click.option(
    "--severity", default=None, type=click.Choice(SEVERITY_CHOICES), help="Incident severity"
)
@click.option("--assignee", default=None, help="Assignee name (e.g., muhammad, willem, jeong)")
@click.option("--summary", default=None, help="Incident summary")
@click.option("--root-cause", default=None, help="Root cause description")
@click.option("--triage-findings", default=None, help="Triage findings")
@click.option("--github-refs", default=None, help="GitHub references")
@click.option("--datadog-refs", default=None, help="Datadog references")
@click.option(
    "--detection-method",
    default=None,
    type=click.Choice(["monitor", "employee", "customer", "alert", "unknown"]),
    help="Detection method",
)
@click.option(
    "--needs-monitoring",
    default=None,
    type=click.Choice(["yes", "no"]),
    help="Needs monitoring flag",
)
@click.option(
    "--needs-human-attention",
    default=None,
    type=click.Choice(["yes", "no"]),
    help="Needs human attention flag",
)
@click.option(
    "--triage-completed",
    default=None,
    type=click.Choice(["yes", "no"]),
    help="Triage completed flag",
)
@click.option(
    "--is-duplicate",
    default=None,
    type=click.Choice(["yes", "no"]),
    help="Is duplicate flag",
)
@click.option("--teams", multiple=True, default=None, help="Team names (repeatable)")
@click.option("--services", multiple=True, default=None, help="Service names (repeatable)")
@click.option(
    "--related-incidents", multiple=True, default=None, help="Related incident IDs (repeatable)"
)
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def update_incident(
    incident_id,
    title,
    status,
    severity,
    assignee,
    summary,
    root_cause,
    triage_findings,
    github_refs,
    datadog_refs,
    detection_method,
    needs_monitoring,
    needs_human_attention,
    triage_completed,
    is_duplicate,
    teams,
    services,
    related_incidents,
    format,
):
    """Update an existing incident."""
    from datadog_api_client.v2.model.incident_update_request import IncidentUpdateRequest
    from datadog_api_client.v2.model.incident_update_data import IncidentUpdateData
    from datadog_api_client.v2.model.incident_update_attributes import IncidentUpdateAttributes
    from datadog_api_client.v2.model.incident_type import IncidentType

    field_opts = [
        summary,
        root_cause,
        triage_findings,
        github_refs,
        datadog_refs,
        detection_method,
        needs_monitoring,
        needs_human_attention,
        triage_completed,
        is_duplicate,
        teams,
        services,
        related_incidents,
    ]
    if not any([title, status, severity, assignee] + field_opts):
        raise click.UsageError(
            "No update fields specified. Use --title, --status, --severity, --assignee, or field options."
        )

    client = get_datadog_client()

    attrs_kwargs = {}
    if title is not None:
        attrs_kwargs["title"] = title
    if assignee is not None:
        attrs_kwargs["assignee"] = assignee

    fields = {}
    if severity is not None:
        fields["severity"] = {"type": "dropdown", "value": severity}
    if fields:
        attrs_kwargs["fields"] = fields

    body = IncidentUpdateRequest(
        data=IncidentUpdateData(
            id=incident_id,
            type=IncidentType("incidents"),
            attributes=IncidentUpdateAttributes(**attrs_kwargs),
        )
    )

    with console.status(f"[cyan]Updating incident {incident_id}...[/cyan]"):
        response = client.incidents.update_incident(incident_id=incident_id, body=body)

    inc = response.data
    attrs = inc.attributes

    # Handle field updates via raw requests if any field options are provided
    field_data = {}
    if status is not None:
        # "state" is the Datadog custom-field key for incident status;
        # IncidentUpdateAttributes does not expose it as a typed attribute.
        field_data["state"] = {"type": "dropdown", "value": status}
    if summary is not None:
        field_data["summary"] = {"type": "textbox", "value": summary}
    if root_cause is not None:
        field_data["root_cause"] = {"type": "textbox", "value": root_cause}
    if triage_findings is not None:
        field_data["triagefindings"] = {"type": "textbox", "value": triage_findings}
    if github_refs is not None:
        field_data["githubreferences"] = {"type": "textbox", "value": github_refs}
    if datadog_refs is not None:
        field_data["datadogreferences"] = {"type": "textbox", "value": datadog_refs}
    if detection_method is not None:
        field_data["detection_method"] = {"type": "dropdown", "value": detection_method}
    if needs_monitoring is not None:
        field_data["needsmonitoring"] = {
            "type": "dropdown",
            "value": needs_monitoring.capitalize(),
        }
    if needs_human_attention is not None:
        field_data["needshumanattention"] = {
            "type": "dropdown",
            "value": needs_human_attention.capitalize(),
        }
    if triage_completed is not None:
        field_data["triagecompleted"] = {
            "type": "dropdown",
            "value": triage_completed.capitalize(),
        }
    if is_duplicate is not None:
        field_data["isduplicate"] = {
            "type": "dropdown",
            "value": is_duplicate.capitalize(),
        }
    if teams:
        field_data["teams"] = {"type": "autocomplete", "value": list(teams)}
    if services:
        field_data["services"] = {"type": "autocomplete", "value": list(services)}
    if related_incidents:
        field_data["relatedincidents"] = {"type": "textarray", "value": list(related_incidents)}

    if field_data:
        config = load_config()
        base_url = f"https://{config.site}/api/v2/incidents"
        headers = {
            "DD-API-KEY": config.api_key,
            "DD-APPLICATION-KEY": config.app_key,
            "Content-Type": "application/json",
        }
        patch_body = {
            "data": {
                "type": "incidents",
                "id": inc.id,
                "attributes": {"fields": field_data},
            }
        }
        try:
            patch_resp = requests.patch(
                f"{base_url}/{inc.id}", headers=headers, json=patch_body, timeout=30
            )
            patch_resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            console.print(f"[yellow]Warning: Field update failed: {e}[/yellow]")

    if format == "json":
        output = {
            "id": inc.id,
            "title": getattr(attrs, "title", ""),
            "status": _stringify_enum(_incident_state(attrs), "unknown"),
            "assignee": getattr(attrs, "assignee", ""),
        }
        click.echo(json.dumps(output))
    else:
        console.print(f"[green]Incident {incident_id} updated[/green]")
        console.print(f"[bold]Title:[/bold] {getattr(attrs, 'title', '')}")
        if assignee:
            console.print(f"[bold]Assignee:[/bold] {assignee}")


@incident.command(name="delete")
@click.argument("incident_id")
@click.option("--confirm", "confirmed", is_flag=True, help="Skip confirmation prompt")
@handle_api_error
def delete_incident(incident_id, confirmed):
    """Delete an incident."""
    if not confirm_action(f"Delete incident {incident_id}?", confirmed):
        console.print("[yellow]Aborted[/yellow]")
        return

    client = get_datadog_client()

    with console.status(f"[cyan]Deleting incident {incident_id}...[/cyan]"):
        client.incidents.delete_incident(incident_id=incident_id)

    console.print(f"[green]Incident {incident_id} deleted[/green]")


@incident.group()
def fields():
    """Incident custom fields."""
    pass


@fields.command(name="get")
@click.argument("incident_id")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def get_fields(incident_id, format):
    """Get custom field values for an incident."""
    config = load_config()

    with console.status(f"[cyan]Fetching incident fields for {incident_id}...[/cyan]"):
        fields_dict = _fetch_custom_fields(incident_id, config)

    if format == "json":
        click.echo(json.dumps({"data": fields_dict}))
    else:
        table = Table(title=f"Fields for {incident_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")

        for key in sorted(fields_dict.keys()):
            table.add_row(key, str(fields_dict[key]))

        console.print(table)


@incident.group()
def todo():
    """Incident todo management."""
    pass


@todo.command(name="add")
@click.argument("incident_id")
@click.option("--content", required=True, help="Todo content")
@click.option("--assignee", multiple=True, default=None, help="Assignee (e.g., @username)")
@click.option("--due-date", default=None, help="Due date (ISO format)")
@handle_api_error
def add_todo(incident_id, content, assignee, due_date):
    """Add a todo to an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    body = {
        "data": {
            "type": "incident_todos",
            "attributes": {
                "content": content,
                "assignees": list(assignee) if assignee else [],
                "due_date": due_date,
            },
        }
    }

    with console.status("[cyan]Creating todo...[/cyan]"):
        resp = requests.post(
            f"{base_url}/{uuid}/relationships/todos", headers=headers, json=body, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()

    todo_id = result.get("data", {}).get("id", "unknown")
    console.print(f"[green]Todo created: {todo_id} — {content}[/green]")


@todo.command(name="list")
@click.argument("incident_id")
@handle_api_error
def list_todos(incident_id):
    """List todos for an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    with console.status("[cyan]Fetching todos...[/cyan]"):
        resp = requests.get(f"{base_url}/{uuid}/relationships/todos", headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()

    todos = result.get("data", [])

    table = Table(title=f"Todos for {incident_id}")
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Content", style="white")
    table.add_column("Assignees", style="dim", width=20)
    table.add_column("Due Date", style="dim", width=20)
    table.add_column("Completed", style="dim", width=10)

    for todo_item in todos:
        attrs = todo_item.get("attributes", {})
        todo_id = todo_item.get("id", "")[:8]
        todo_content = attrs.get("content", "")
        assignees = ", ".join(attrs.get("assignees", []))
        due_date = attrs.get("due_date") or "N/A"
        completed = "Yes" if attrs.get("completed") else "No"
        table.add_row(todo_id, todo_content, assignees, due_date, completed)

    console.print(table)


@todo.command(name="complete")
@click.argument("incident_id")
@click.argument("todo_id")
@handle_api_error
def complete_todo(incident_id, todo_id):
    """Mark a todo as complete."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    completed_at = datetime.now(timezone.utc).isoformat()
    body = {
        "data": {
            "type": "incident_todos",
            "id": todo_id,
            "attributes": {"completed": completed_at},
        }
    }

    with console.status("[cyan]Marking todo complete...[/cyan]"):
        resp = requests.patch(
            f"{base_url}/{uuid}/relationships/todos/{todo_id}",
            headers=headers,
            json=body,
            timeout=30,
        )
        resp.raise_for_status()

    console.print(f"[green]Todo {todo_id} marked complete[/green]")


@todo.command(name="delete")
@click.argument("incident_id")
@click.argument("todo_id")
@handle_api_error
def delete_todo(incident_id, todo_id):
    """Delete a todo from an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    with console.status("[cyan]Deleting todo...[/cyan]"):
        resp = requests.delete(
            f"{base_url}/{uuid}/relationships/todos/{todo_id}", headers=headers, timeout=30
        )
        resp.raise_for_status()

    console.print("[green]Todo deleted[/green]")


@incident.group()
def impact():
    """Incident impact management."""
    pass


@impact.command(name="add")
@click.argument("incident_id")
@click.option("--description", required=True, help="Impact description")
@click.option("--start", required=True, help="Start time (ISO format)")
@click.option("--end", default=None, help="End time (ISO format)")
@handle_api_error
def add_impact(incident_id, description, start, end):
    """Add an impact to an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    body = {
        "data": {
            "type": "incident_impacts",
            "attributes": {
                "description": description,
                "start_at": start,
                "end_at": end,
            },
        }
    }

    with console.status("[cyan]Creating impact...[/cyan]"):
        resp = requests.post(f"{base_url}/{uuid}/impacts", headers=headers, json=body, timeout=30)
        resp.raise_for_status()
        result = resp.json()

    impact_id = result.get("data", {}).get("id", "unknown")
    console.print(f"[green]Impact created: {impact_id}[/green]")


@impact.command(name="list")
@click.argument("incident_id")
@handle_api_error
def list_impacts(incident_id):
    """List impacts for an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    with console.status("[cyan]Fetching impacts...[/cyan]"):
        resp = requests.get(f"{base_url}/{uuid}/impacts", headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()

    impacts = result.get("data", [])

    table = Table(title=f"Impacts for {incident_id}")
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Description", style="white")
    table.add_column("Start", style="dim", width=25)
    table.add_column("End", style="dim", width=25)

    for impact_item in impacts:
        attrs = impact_item.get("attributes", {})
        impact_id = impact_item.get("id", "")[:8]
        description = attrs.get("description", "")
        start = attrs.get("start_at", "N/A")
        end = attrs.get("end_at") or "N/A"
        table.add_row(impact_id, description, start, end)

    console.print(table)


@impact.command(name="delete")
@click.argument("incident_id")
@click.argument("impact_id")
@handle_api_error
def delete_impact(incident_id, impact_id):
    """Delete an impact from an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    with console.status("[cyan]Deleting impact...[/cyan]"):
        resp = requests.delete(
            f"{base_url}/{uuid}/impacts/{impact_id}", headers=headers, timeout=30
        )
        resp.raise_for_status()

    console.print("[green]Impact deleted[/green]")


@incident.group()
def attachment():
    """Incident attachment management."""
    pass


@attachment.command(name="add")
@click.argument("incident_id")
@click.option("--url", required=True, help="Attachment URL")
@click.option("--title", required=True, help="Attachment title")
@click.option(
    "--type", type=click.Choice(["link", "postmortem"]), default="link", help="Attachment type"
)
@handle_api_error
def add_attachment(incident_id, url, title, type):
    """Add an attachment to an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    body = {
        "data": {
            "type": "incident_attachments",
            "attributes": {
                "attachment_type": type,
                "attachment": {
                    "documentUrl": url,
                    "title": title,
                },
            },
        }
    }

    with console.status("[cyan]Creating attachment...[/cyan]"):
        resp = requests.post(
            f"{base_url}/{uuid}/attachments", headers=headers, json=body, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()

    attachment_id = result.get("data", {}).get("id", "unknown")
    console.print(f"[green]Attachment created: {attachment_id} — {title}[/green]")


@attachment.command(name="list")
@click.argument("incident_id")
@handle_api_error
def list_attachments(incident_id):
    """List attachments for an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    with console.status("[cyan]Fetching attachments...[/cyan]"):
        resp = requests.get(f"{base_url}/{uuid}/attachments", headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()

    attachments = result.get("data", [])

    table = Table(title=f"Attachments for {incident_id}")
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Type", style="yellow", width=12)
    table.add_column("Title", style="white")
    table.add_column("URL", style="dim")

    for att_item in attachments:
        attrs = att_item.get("attributes", {})
        att_id = att_item.get("id", "")[:8]
        att_type = attrs.get("attachment_type", "")
        attachment = attrs.get("attachment", {})
        att_title = attachment.get("title", "")
        att_url = attachment.get("documentUrl", "")
        table.add_row(att_id, att_type, att_title, att_url)

    console.print(table)


@attachment.command(name="delete")
@click.argument("incident_id")
@click.argument("attachment_id")
@handle_api_error
def delete_attachment(incident_id, attachment_id):
    """Delete an attachment from an incident."""
    client = get_datadog_client()

    with console.status(f"[cyan]Resolving incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)
    uuid = response.data.id

    config = load_config()
    base_url = f"https://{config.site}/api/v2/incidents"
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }

    with console.status("[cyan]Deleting attachment...[/cyan]"):
        resp = requests.delete(
            f"{base_url}/{uuid}/attachments/{attachment_id}", headers=headers, timeout=30
        )
        resp.raise_for_status()

    console.print("[green]Attachment deleted[/green]")


@incident.group()
def timeline():
    """Incident timeline commands."""
    pass


@timeline.command(name="list")
@click.argument("incident_id")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def list_timeline(incident_id, format):
    """List timeline cells for an incident.

    Returns all timeline entries in chronological order: markdown notes posted
    by agents or humans, and system status change events. This is the primary
    source of truth for understanding what triggered an incident and what was
    observed during triage.
    """
    config = load_config()
    headers = {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
    }
    url = f"https://api.{config.site}/api/v2/incidents/{incident_id}/timeline"

    with console.status(f"[cyan]Fetching timeline for {incident_id}...[/cyan]"):
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    cells = data.get("data", [])

    if format == "json":
        output = []
        for cell in cells:
            attrs = cell.get("attributes", {})
            output.append(
                {
                    "id": cell.get("id", ""),
                    "cell_type": attrs.get("cell_type", ""),
                    "created": attrs.get("created", ""),
                    "modified": attrs.get("modified", ""),
                    "content": attrs.get("content", {}),
                }
            )
        click.echo(json.dumps({"data": output}))
    else:
        console.print(f"\n[bold cyan]Timeline for {incident_id}[/bold cyan]")
        console.print(f"[dim]{len(cells)} cells[/dim]\n")
        for cell in cells:
            attrs = cell.get("attributes", {})
            cell_type = attrs.get("cell_type", "")
            created = attrs.get("created", "")[:19]
            content = attrs.get("content", {})

            console.print(f"[dim]{created}[/dim] [yellow]{cell_type}[/yellow]")

            if cell_type == "markdown":
                md_content = content.get("content", "")
                console.print(md_content)
            elif cell_type == "incident_status_change":
                action = content.get("action", "")
                after = content.get("after", {})
                before = content.get("before", {})
                if action == "created":
                    console.print(
                        f"  Incident created — title: {after.get('title', '')} severity: {after.get('severity', '')}"
                    )
                elif action == "updated":
                    for key in set(list(before.keys()) + list(after.keys())):
                        if before.get(key) != after.get(key):
                            console.print(
                                f"  {key}: [red]{before.get(key, '')}[/red] → [green]{after.get(key, '')}[/green]"
                            )
            else:
                console.print(f"  {json.dumps(content)[:200]}")
            console.print()
