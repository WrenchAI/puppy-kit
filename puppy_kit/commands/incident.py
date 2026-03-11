"""Incident management commands."""

from datetime import datetime, timedelta, timezone
import json
import re
import warnings

import click
from rich.console import Console
from rich.table import Table
from puppy_kit.client import get_datadog_client
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.confirm import confirm_action

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
@click.option("--page-size", type=int, default=10, help="Page size for results")
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
                sort=sort,
                page_size=effective_page_size,
                page_offset=page_offset,
            )

            incidents = list(getattr(response, "included", []) or [])
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

                last_incident = incidents[-1]
                last_attrs = getattr(last_incident, "attributes", None)
                last_created = _coerce_utc_datetime(_get_attr(last_attrs, "created", None))
                if last_created is not None and last_created < cutoff:
                    break
            else:
                all_incidents.extend(incidents)

            pagination = getattr(getattr(response, "meta", None), "pagination", None)
            next_offset = getattr(pagination, "next_offset", None)
            if next_offset is None:
                break

            page_offset = int(next_offset)

    if format == "json":
        output = []
        for inc in all_incidents:
            attrs = getattr(inc, "attributes", None)
            output.append(
                {
                    "id": _get_attr(inc, "id", ""),
                    "title": _get_attr(attrs, "title", ""),
                    "severity": _stringify_enum(_get_attr(attrs, "severity", "unknown")),
                    "status": _stringify_enum(_get_attr(attrs, "status", "unknown")),
                    "customer_impacted": _get_attr(attrs, "customer_impacted", "unknown"),
                    "public_id": _get_attr(inc, "public_id", "unknown"),
                    "detected": _stringify_datetime(_get_attr(attrs, "detected", "")),
                    "resolved": _stringify_datetime(_get_attr(attrs, "resolved", "")),
                    "created": _stringify_datetime(_get_attr(attrs, "created", "")),
                    "modified": _stringify_datetime(_get_attr(attrs, "modified", "")),
                }
            )
        print(json.dumps(output, indent=2))
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
            status_str = _stringify_enum(_get_attr(attrs, "status", "unknown"))
            severity_str = _stringify_enum(_get_attr(attrs, "severity", "unknown"))
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


@incident.command(name="get")
@click.argument("incident_id")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def get_incident(incident_id, format):
    """Get incident details."""
    client = get_datadog_client()

    with console.status(f"[cyan]Fetching incident {incident_id}...[/cyan]"):
        response = client.incidents.get_incident(incident_id=incident_id)

    inc = response.data
    attrs = inc.attributes

    if format == "json":
        output = {
            "id": inc.id,
            "title": getattr(attrs, "title", ""),
            "severity": _stringify_enum(getattr(attrs, "severity", "unknown")),
            "status": _stringify_enum(getattr(attrs, "status", "unknown")),
            "customer_impacted": getattr(attrs, "customer_impacted", "unknown"),
            "public_id": getattr(inc, "public_id", "unknown"),
            "detected": _stringify_datetime(getattr(attrs, "detected", "")),
            "resolved": _stringify_datetime(getattr(attrs, "resolved", "")),
            "created": _stringify_datetime(getattr(attrs, "created", "")),
            "modified": _stringify_datetime(getattr(attrs, "modified", "")),
        }
        print(json.dumps(output, indent=2))
    else:
        console.print(f"\n[bold cyan]Incident {inc.id}[/bold cyan]")
        console.print(f"[bold]Title:[/bold] {getattr(attrs, 'title', '')}")

        severity_str = _stringify_enum(getattr(attrs, "severity", "unknown"))
        console.print(f"[bold]Severity:[/bold] [yellow]{severity_str}[/yellow]")

        status_str = _stringify_enum(getattr(attrs, "status", "unknown"))
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


@incident.command(name="create")
@click.option("--title", required=True, help="Incident title")
@click.option(
    "--severity",
    type=click.Choice(SEVERITY_CHOICES),
    required=True,
    help="Incident severity",
)
@click.option("--team", required=True, help="Team name for the 'teams' autocomplete field")
@click.option("--assignee", default=None, help="Assignee user ID (UUID) to set as commander")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def create_incident(title, severity, team, assignee, format):
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

    client = get_datadog_client()

    fields = {
        "severity": {"type": "dropdown", "value": severity},
        "teams": {"type": "autocomplete", "value": [team]},
    }

    relationships = None
    if assignee:
        relationships = IncidentCreateRelationships(
            commander_user=NullableRelationshipToUser(
                data=NullableRelationshipToUserData(type="users", id=assignee)
            )
        )

    data_kwargs = dict(
        type="incidents",
        attributes=IncidentCreateAttributes(
            title=title,
            customer_impacted=False,
            fields=fields,
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
            "severity": _stringify_enum(getattr(attrs, "severity", severity or "unknown")),
            "status": _stringify_enum(getattr(attrs, "status", "unknown")),
        }
        print(json.dumps(output, indent=2))
    else:
        console.print(f"[green]Incident {inc.id} created[/green]")
        console.print(f"[bold]Title:[/bold] {getattr(attrs, 'title', '')}")
        console.print(
            f"[bold]Severity:[/bold] {_stringify_enum(getattr(attrs, 'severity', severity or 'unknown'))}"
        )
        console.print(
            f"[bold]Status:[/bold] {_stringify_enum(getattr(attrs, 'status', 'unknown'))}"
        )


@incident.command(name="update")
@click.argument("incident_id")
@click.option("--title", default=None, help="New incident title")
@click.option("--status", default=None, type=click.Choice(STATUS_CHOICES), help="Incident status")
@click.option(
    "--severity", default=None, type=click.Choice(SEVERITY_CHOICES), help="Incident severity"
)
@click.option("--assignee", default=None, help="Assignee name (e.g., muhammad, willem, jeong)")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def update_incident(incident_id, title, status, severity, assignee, format):
    """Update an existing incident."""
    from datadog_api_client.v2.model.incident_update_request import IncidentUpdateRequest
    from datadog_api_client.v2.model.incident_update_data import IncidentUpdateData
    from datadog_api_client.v2.model.incident_update_attributes import IncidentUpdateAttributes
    from datadog_api_client.v2.model.incident_field_attributes import IncidentFieldAttributes
    from datadog_api_client.v2.model.incident_field_attributes_single_value_type import (
        IncidentFieldAttributesSingleValueType,
    )

    if not any([title, status, severity, assignee]):
        raise click.UsageError(
            "No update fields specified. Use --title, --status, --severity, or --assignee."
        )

    client = get_datadog_client()

    attrs_kwargs = {}
    if title is not None:
        attrs_kwargs["title"] = title
    if assignee is not None:
        attrs_kwargs["assignee"] = assignee

    fields = {}
    if status is not None:
        fields["state"] = IncidentFieldAttributes(
            type=IncidentFieldAttributesSingleValueType.DROPDOWN,
            value=status,
        )
    if severity is not None:
        fields["severity"] = {"type": "dropdown", "value": severity}
    if fields:
        attrs_kwargs["fields"] = fields

    body = IncidentUpdateRequest(
        data=IncidentUpdateData(
            id=incident_id,
            type="incidents",
            attributes=IncidentUpdateAttributes(**attrs_kwargs),
        )
    )

    with console.status(f"[cyan]Updating incident {incident_id}...[/cyan]"):
        response = client.incidents.update_incident(incident_id=incident_id, body=body)

    inc = response.data
    attrs = inc.attributes

    if format == "json":
        output = {
            "id": inc.id,
            "title": getattr(attrs, "title", ""),
            "status": _stringify_enum(getattr(attrs, "status", "unknown")),
            "assignee": getattr(attrs, "assignee", ""),
        }
        print(json.dumps(output, indent=2))
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
