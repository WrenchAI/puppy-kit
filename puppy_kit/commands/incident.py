"""Incident management commands."""

import click
import json
import warnings
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
    help="Filter by status",
)
@click.option("--page-size", type=int, default=10, help="Page size for results")
@click.option("--all-pages", is_flag=True, help="Fetch all pages (paginate through all incidents)")
@handle_api_error
def list_incidents(format, status, page_size, all_pages):
    """List all incidents, with optional pagination."""
    client = get_datadog_client()

    all_incidents = []
    page_offset = 0

    with console.status("[cyan]Fetching incidents...[/cyan]"):
        while True:
            response = client.incidents.list_incidents(page_size=page_size, page_offset=page_offset)

            incidents = response.data if response.data else []
            if not incidents:
                break

            all_incidents.extend(incidents)

            if not all_pages or len(incidents) < page_size:
                break

            page_offset += page_size

    # Filter by status if provided
    if status:
        all_incidents = [
            inc
            for inc in all_incidents
            if _stringify_enum(getattr(inc.attributes, "status", "unknown")) == status
        ]

    if format == "json":
        output = []
        for inc in all_incidents:
            attrs = inc.attributes
            output.append(
                {
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
            attrs = inc.attributes
            status_str = _stringify_enum(getattr(attrs, "status", "unknown"))
            severity_str = _stringify_enum(getattr(attrs, "severity", "unknown"))
            status_color = {
                "active": "red",
                "stable": "yellow",
                "resolved": "green",
            }.get(status_str, "white")

            table.add_row(
                str(inc.id),
                str(getattr(attrs, "title", "")),
                severity_str,
                f"[{status_color}]{status_str}[/{status_color}]",
                _impact_label(getattr(attrs, "customer_impacted", "unknown")),
                _stringify_datetime(getattr(attrs, "created", "")),
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

    if not any([title, status, severity, assignee]):
        raise click.UsageError(
            "No update fields specified. Use --title, --status, --severity, or --assignee."
        )

    client = get_datadog_client()

    attrs_kwargs = {}
    if title is not None:
        attrs_kwargs["title"] = title
    if status is not None:
        attrs_kwargs["status"] = status
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
