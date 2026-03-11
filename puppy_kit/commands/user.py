"""User management commands."""

import click
import json
from rich.console import Console
from rich.table import Table
from puppy_kit.client import get_datadog_client
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.confirm import confirm_action
from puppy_kit.utils.format import json_list_response

console = Console()


@click.group()
def user():
    """User management commands."""
    pass


@user.command(name="list")
@click.option("--limit", type=click.IntRange(min=1), default=None, help="Max users to fetch (alias for --page-size)")
@click.option(
    "--page-size",
    type=click.IntRange(min=1),
    default=100,
    show_default=True,
    help="Number of users to fetch per page",
)
@click.option("--filter", "filter_text", default=None, help="Filter users by name or email")
@click.option(
    "--filter-status",
    default=None,
    help="Filter by status: Active, Pending, Disabled (comma-separated)",
)
@click.option(
    "--sort",
    type=click.Choice(["name", "modified_at", "user_count"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sort field",
)
@click.option(
    "--all-pages/--no-all-pages",
    default=True,
    show_default=True,
    help="Fetch all pages of users",
)
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def list_users(limit, page_size, filter_text, filter_status, sort, all_pages, format):
    """List all users in the organization."""
    client = get_datadog_client()

    # Use limit as alias for page_size if provided
    if limit is not None:
        page_size = limit

    with console.status("[cyan]Fetching users...[/cyan]"):
        users_data = []
        page_number = 0
        while True:
            kwargs = {
                "page_size": page_size,
                "page_number": page_number,
                "sort": sort,
            }
            if filter_text:
                kwargs["filter"] = filter_text
            if filter_status:
                kwargs["filter_status"] = filter_status

            response = client.users.list_users(**kwargs)
            page_users = list(response.data or [])
            users_data.extend(page_users)

            if not all_pages or len(page_users) < page_size:
                break
            page_number += 1

    if format == "json":
        output = []
        for u in users_data:
            attrs = getattr(u, "attributes", None)
            output.append(
                {
                    "id": u.id,
                    "name": getattr(attrs, "name", None),
                    "email": getattr(attrs, "email", None),
                    "handle": getattr(attrs, "handle", None),
                    "status": getattr(attrs, "status", None),
                    "title": getattr(attrs, "title", None),
                    "disabled": getattr(attrs, "disabled", None),
                    "created_at": str(getattr(attrs, "created_at", None)),
                }
            )
        click.echo(json.dumps(json_list_response(output)))
    else:
        table = Table(title="Users")
        table.add_column("ID", style="dim")
        table.add_column("Status", style="yellow")
        table.add_column("Email", style="white")
        table.add_column("Name", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Created", style="dim")

        for u in users_data:
            attrs = getattr(u, "attributes", None)
            user_id = getattr(u, "id", "") or ""
            status = getattr(attrs, "status", "") or ""
            email = getattr(attrs, "email", "") or ""
            name = getattr(attrs, "name", "") or ""
            title = getattr(attrs, "title", "") or ""
            created_at = str(getattr(attrs, "created_at", "")) or ""

            table.add_row(user_id, status, email, name, title, created_at)

        console.print(table)
        console.print(f"\n[dim]Total users: {len(users_data)}[/dim]")


@user.command(name="get")
@click.argument("user_id")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def get_user(user_id, format):
    """Get user details by ID."""
    client = get_datadog_client()

    with console.status(f"[cyan]Fetching user {user_id}...[/cyan]"):
        response = client.users.get_user(user_id=user_id)

    u = response.data
    attrs = getattr(u, "attributes", None)
    user_id_value = getattr(u, "id", "N/A")

    if format == "json":
        output = {
            "id": user_id_value,
            "name": getattr(attrs, "name", None),
            "email": getattr(attrs, "email", None),
            "handle": getattr(attrs, "handle", None),
            "status": getattr(attrs, "status", None),
            "disabled": getattr(attrs, "disabled", None),
            "created_at": str(getattr(attrs, "created_at", None)),
        }
        click.echo(json.dumps(json_list_response(output)))
    else:
        console.print(f"\n[bold cyan]User {user_id_value}[/bold cyan]")
        console.print(f"[bold]Name:[/bold] {getattr(attrs, 'name', 'N/A')}")
        console.print(f"[bold]Email:[/bold] {getattr(attrs, 'email', 'N/A')}")
        console.print(f"[bold]Handle:[/bold] {getattr(attrs, 'handle', 'N/A')}")
        console.print(f"[bold]Status:[/bold] {getattr(attrs, 'status', 'N/A')}")
        console.print(f"[bold]Disabled:[/bold] {getattr(attrs, 'disabled', 'N/A')}")
        console.print(f"[bold]Created At:[/bold] {getattr(attrs, 'created_at', 'N/A')}")


@user.command(name="invite")
@click.option("--email", required=True, help="Email address to invite")
@click.option("--role", default=None, help="Role to assign to the invited user")
@click.option(
    "--format", type=click.Choice(["json", "table"]), default="table", help="Output format"
)
@handle_api_error
def invite_user(email, role, format):
    """Send a user invitation."""
    from datadog_api_client.v2.model.user_invitation_data import UserInvitationData
    from datadog_api_client.v2.model.user_invitation_relationships import (
        UserInvitationRelationships,
    )
    from datadog_api_client.v2.model.user_invitations_request import UserInvitationsRequest
    from datadog_api_client.v2.model.relationship_to_user import RelationshipToUser
    from datadog_api_client.v2.model.relationship_to_user_data import RelationshipToUserData
    from datadog_api_client.v2.model.user_create_request import UserCreateRequest
    from datadog_api_client.v2.model.user_create_data import UserCreateData
    from datadog_api_client.v2.model.user_create_attributes import UserCreateAttributes
    from datadog_api_client.v2.model.users_type import UsersType

    client = get_datadog_client()

    # First create the user
    user_attributes = UserCreateAttributes(email=email)
    user_data = UserCreateData(
        type=UsersType("users"),
        attributes=user_attributes,
    )
    user_request = UserCreateRequest(data=user_data)

    with console.status(f"[cyan]Creating user and sending invitation to {email}...[/cyan]"):
        create_response = client.users.create_user(body=user_request)
        new_user = create_response.data

        # Now send invitation
        invitation_data = UserInvitationData(
            type="user_invitations",
            relationships=UserInvitationRelationships(
                user=RelationshipToUser(
                    data=RelationshipToUserData(
                        id=new_user.id,
                        type=UsersType("users"),
                    )
                )
            ),
        )
        body = UserInvitationsRequest(data=[invitation_data])
        client.users.send_invitations(body=body)

    if format == "json":
        output = {
            "email": email,
            "user_id": new_user.id,
            "status": "invitation_sent",
        }
        click.echo(json.dumps(json_list_response(output)))
    else:
        console.print(f"[green]Invitation sent to {email}[/green]")
        console.print(f"[dim]User ID: {new_user.id}[/dim]")


@user.command(name="disable")
@click.argument("user_id")
@click.option("--confirm", "confirmed", is_flag=True, help="Skip confirmation prompt")
@handle_api_error
def disable_user(user_id, confirmed):
    """Disable a user by ID."""
    if not confirm_action(f"Disable user {user_id}?", confirmed):
        console.print("[yellow]Aborted[/yellow]")
        return

    client = get_datadog_client()

    with console.status(f"[cyan]Disabling user {user_id}...[/cyan]"):
        client.users.disable_user(user_id=user_id)

    console.print(f"[green]User {user_id} disabled[/green]")
