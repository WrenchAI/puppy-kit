"""APM (Application Performance Monitoring) commands."""

import click
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from puppy_kit.client import get_datadog_client
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.time import parse_time_range
from puppy_kit.utils.format import truncate, json_list_response
from puppy_kit.utils.spans import aggregate_spans

console = Console()


@click.group()
def apm():
    """APM (Application Performance Monitoring) commands."""
    pass


@apm.command(name="services")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@handle_api_error
def list_services(format):
    """List all APM services."""
    client = get_datadog_client()

    with console.status("[cyan]Fetching APM services...[/cyan]"):
        response = client.service_definitions.list_service_definitions(page_size=100)

    services = []
    for item in response.data or []:
        schema = item.attributes.schema
        services.append(
            {
                "name": schema.dd_service,
                "team": getattr(schema, "team", ""),
                "type": getattr(schema, "type", ""),
                "languages": getattr(schema, "languages", []),
            }
        )

    if format == "json":
        click.echo(json.dumps(json_list_response(services)))
    else:
        table = Table(title="APM Services")
        table.add_column("Service", style="cyan")
        table.add_column("Team", style="white")
        table.add_column("Type", style="dim")
        table.add_column("Languages", style="yellow")
        for svc in sorted(services, key=lambda s: s["name"]):
            table.add_row(
                svc["name"],
                svc["team"],
                svc["type"],
                ", ".join(svc["languages"]) if svc["languages"] else "",
            )
        console.print(table)
        console.print(f"\n[dim]Total services: {len(services)}[/dim]")


@apm.command(name="traces")
@click.argument("service")
@click.option("--from", "from_time", default="1h", help="Start time (e.g., 1h, 24h, 7d)")
@click.option("--to", "to_time", default="now", help="End time")
@click.option("--limit", default=100, type=int, help="Max traces [default: 100]")
@click.option("--filter", "extra_filter", help="Additional filter query")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@click.option("--verbose", is_flag=True, default=False, help="Show all span details")
@handle_api_error
def search_traces(service, from_time, to_time, limit, extra_filter, format, verbose):
    """Search traces for a service.

    Rate limit: 300 requests/hour for spans API.
    """
    client = get_datadog_client()

    # Parse time range
    from_ts, to_ts = parse_time_range(from_time, to_time)
    from_str = datetime.fromtimestamp(from_ts).isoformat() + "Z"
    to_str = datetime.fromtimestamp(to_ts).isoformat() + "Z"

    # Build query
    query = f"service:{service}"
    if extra_filter:
        query = f"{query} {extra_filter}"

    with console.status(f"[cyan]Searching traces for {service}...[/cyan]"):
        response = client.spans.list_spans_get(
            filter_query=query, filter_from=from_str, filter_to=to_str, page_limit=limit
        )

    spans = response.data if response.data else []

    if format == "json":
        output = []
        for span in spans:
            attrs = span.attributes
            duration_ms = (attrs.duration / 1_000_000) if hasattr(attrs, "duration") else 0

            span_dict = {
                "trace_id": attrs.trace_id,
                "span_id": attrs.span_id,
                "service": attrs.service,
                "resource": attrs.resource_name,
                "duration_ms": round(duration_ms, 2),
                "timestamp": (attrs.start_timestamp.isoformat() if attrs.start_timestamp else None),
            }
            if verbose:
                # Include all details
                span_dict["span_object"] = span.to_dict()
            output.append(span_dict)
        click.echo(json.dumps(json_list_response(output)))
    else:
        table = Table(title=f"Traces for {service}")
        table.add_column("Trace ID", style="cyan", width=18)
        table.add_column("Resource", style="white", min_width=30)
        table.add_column("Duration (ms)", justify="right", style="yellow", width=15)
        if verbose:
            table.add_column("Status", style="white", width=10)
        table.add_column("Time", style="dim", width=12)

        for span in spans:
            attrs = span.attributes
            duration_ms = (attrs.duration / 1_000_000) if hasattr(attrs, "duration") else 0
            time_str = (
                attrs.start_timestamp.strftime("%H:%M:%S") if attrs.start_timestamp else "N/A"
            )

            row_data = [
                attrs.trace_id[:16] + "..",
                truncate(attrs.resource_name, 80),
                f"{duration_ms:.2f}",
            ]
            if verbose:
                status = getattr(attrs, "status", "unknown")
                row_data.append(status)
            row_data.append(time_str)
            table.add_row(*row_data)

        console.print(table)
        console.print(f"\n[dim]Total traces: {len(spans)}[/dim]")


@apm.command(name="analytics")
@click.argument("service")
@click.option("--from", "from_time", default="1h", help="Start time (e.g., 1h, 24h, 7d)")
@click.option("--to", "to_time", default="now", help="End time")
@click.option("--metric", default="count", help="Metric (count, p99, avg, sum)")
@click.option("--group-by", help="Group by field (e.g., resource_name, @http.status_code)")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@handle_api_error
def analytics(service, from_time, to_time, metric, group_by, format):
    """APM analytics and aggregations.

    Compute metrics (count, p99, avg, sum) across traces, optionally grouped by dimensions.
    """
    client = get_datadog_client()

    # Parse time range
    from_ts, to_ts = parse_time_range(from_time, to_time)
    from_str = datetime.fromtimestamp(from_ts).isoformat() + "Z"
    to_str = datetime.fromtimestamp(to_ts).isoformat() + "Z"

    # Build filter (as dict)
    filter_dict = {"query": f"service:{service}", "from": from_str, "to": to_str}

    # Configure compute (as dict)
    if metric == "count":
        compute_dict = {"aggregation": "count"}
    elif metric == "p99":
        compute_dict = {"aggregation": "pc99", "metric": "@duration"}
    elif metric == "avg":
        compute_dict = {"aggregation": "avg", "metric": "@duration"}
    elif metric == "sum":
        compute_dict = {"aggregation": "sum", "metric": "@duration"}
    else:
        compute_dict = {"aggregation": "count"}

    # Configure group-by (as list of dicts)
    group_by_list = [{"facet": group_by}] if group_by else []

    with console.status(f"[cyan]Computing analytics for {service}...[/cyan]"):
        response = aggregate_spans(client, filter_dict, [compute_dict], group_by_list)

    buckets = response.data.buckets if response.data else []

    if format == "json":
        output = []
        for bucket in buckets:
            result = bucket.by.copy() if bucket.by else {}
            # Extract metric value
            if bucket.computes:
                value = list(bucket.computes.values())[0]
                # Convert duration from ns to ms
                if metric in ["p99", "avg", "sum"]:
                    result[metric] = round(value / 1_000_000, 2)
                else:
                    result[metric] = value
            output.append(result)
        click.echo(json.dumps(json_list_response(output)))
    else:
        title = f"Analytics for {service} ({metric})"
        if group_by:
            title += f" by {group_by}"

        table = Table(title=title)
        if group_by:
            table.add_column(group_by.replace("@", ""), style="cyan")

        metric_label = metric.upper()
        if metric in ["p99", "avg", "sum"]:
            metric_label += " (ms)"
        table.add_column(metric_label, justify="right", style="yellow")

        for bucket in buckets:
            row = []
            if bucket.by and group_by:
                row.append(str(bucket.by.get(group_by, "N/A")))

            if bucket.computes:
                value = list(bucket.computes.values())[0]
                if metric in ["p99", "avg", "sum"]:
                    value = value / 1_000_000
                row.append(f"{value:.2f}")

            table.add_row(*row)

        console.print(table)
        console.print(f"\n[dim]Total groups: {len(buckets)}[/dim]")
