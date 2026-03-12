"""Metric query commands."""

import click
import json
from datetime import datetime, timedelta, timezone
from rich.console import Console
from rich.table import Table
from rich.markup import escape
from puppy_kit.client import get_datadog_client
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.time import parse_time_range
from puppy_kit.utils.format import json_list_response

console = Console()


@click.group()
def metric():
    """Metric query commands."""
    pass


@metric.command(name="query")
@click.argument("query")
@click.option("--from", "from_time", default="1h", help="Start time (e.g., 1h, 24h, 7d)")
@click.option("--to", "to_time", default="now", help="End time")
@click.option(
    "--limit", default=100, type=int, help="Max points to show in verbose mode [default: 100]"
)
@click.option(
    "--format", type=click.Choice(["json", "table", "csv"]), default="table", help="Output format"
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Show individual data points instead of summary statistics",
)
@handle_api_error
def query_metric(query, from_time, to_time, limit, format, verbose):
    """Query metrics."""
    client = get_datadog_client()

    from_ts, to_ts = parse_time_range(from_time, to_time)

    with console.status(f"[cyan]Querying metric: {query}...[/cyan]"):
        result = client.metrics.query_metrics(_from=from_ts, to=to_ts, query=query)

    if format == "json":
        output_list = []
        if result.series:
            for series in result.series:
                output_list.append(series)
        click.echo(json.dumps(json_list_response(output_list)))
    elif format == "csv":
        # CSV output for scripting
        if result.series:
            for series in result.series:
                metric_name = series.get("metric", "unknown")
                for point in series.get("pointlist", []):
                    timestamp, value = point.value
                    print(f"{timestamp},{metric_name},{value}")
    else:
        # Table format
        if not result.series:
            console.print("[yellow]No data found for query[/yellow]")
            return

        if verbose:
            # Verbose mode: show individual data points
            for series in result.series:
                metric_name = escape(series.get("metric", "unknown"))
                table = Table(title=f"Metric: {metric_name}")
                table.add_column("Timestamp", style="cyan")
                table.add_column("Value", style="green", justify="right")

                all_points = series.get("pointlist", [])
                points = all_points[-limit:]

                for point in points:
                    timestamp, value = point.value
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    table.add_row(dt.strftime("%Y-%m-%d %H:%M:%S"), f"{value:.2f}")

                console.print(table)
                console.print(f"[dim]Total points: {len(all_points)}[/dim]\n")
        else:
            # Summary mode: one row per series with aggregate stats
            table = Table(title="Metric Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Points", style="yellow", justify="right")
            table.add_column("Min", style="green", justify="right")
            table.add_column("Max", style="green", justify="right")
            table.add_column("Avg", style="green", justify="right")
            table.add_column("Latest", style="magenta", justify="right")
            table.add_column("Trend", style="blue", justify="center")

            for series in result.series:
                metric_name = series.get("metric", "unknown")
                all_points = series.get("pointlist", [])

                if not all_points:
                    # Empty pointlist
                    table.add_row(metric_name, "0", "—", "—", "—", "—", "—")
                    continue

                # Extract values, filtering out None
                values = []
                for point in all_points:
                    try:
                        _, value = point.value
                        if value is not None:
                            values.append(value)
                    except (ValueError, TypeError, AttributeError):
                        pass

                if not values:
                    # No valid values
                    table.add_row(metric_name, str(len(all_points)), "—", "—", "—", "—", "—")
                    continue

                # Compute statistics
                min_val = min(values)
                max_val = max(values)
                avg_val = sum(values) / len(values)
                latest_val = values[-1]

                # Compute trend (first half avg vs second half avg)
                mid = len(values) // 2
                if mid > 0:
                    first_half = values[:mid]
                    second_half = values[mid:]
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)

                    if first_avg > 0:
                        pct_change = (second_avg - first_avg) / first_avg
                        if pct_change > 0.05:
                            trend = "↑"
                        elif pct_change < -0.05:
                            trend = "↓"
                        else:
                            trend = "→"
                    else:
                        trend = "→"
                else:
                    trend = "→"

                # Format for display
                points_count = len(all_points)
                min_str = f"{min_val:.2f}"
                max_str = f"{max_val:.2f}"
                avg_str = f"{avg_val:.2f}"
                latest_str = f"{latest_val:.2f}"

                table.add_row(
                    metric_name, str(points_count), min_str, max_str, avg_str, latest_str, trend
                )

            console.print(table)


@metric.command(name="search")
@click.argument("query")
@click.option("--limit", default=50, help="Maximum results to show")
@handle_api_error
def search_metrics(query, limit):
    """Search available metrics."""
    client = get_datadog_client()

    with console.status(f"[cyan]Searching metrics: {query}...[/cyan]"):
        from_ts = int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp())
        results = client.metrics.list_active_metrics(_from=from_ts)

    if results.metrics:
        results.metrics = [m for m in results.metrics if query.lower() in m.lower()]

    if not results.metrics:
        console.print("[yellow]No metrics found[/yellow]")
        return

    console.print(f"\n[bold]Found {len(results.metrics)} metrics:[/bold]")
    for metric in results.metrics[:limit]:
        console.print(f"  • {metric}")

    if len(results.metrics) > limit:
        console.print(f"\n[dim]... and {len(results.metrics) - limit} more[/dim]")


@metric.command(name="metadata")
@click.argument("metric_name")
@handle_api_error
def get_metric_metadata(metric_name):
    """Get metric metadata."""
    client = get_datadog_client()

    with console.status(f"[cyan]Fetching metadata for {metric_name}...[/cyan]"):
        metadata = client.metrics.get_metric_metadata(metric_name=metric_name)

    console.print(f"\n[bold cyan]Metric: {metric_name}[/bold cyan]")
    if hasattr(metadata, "description") and metadata.description:
        console.print(f"[bold]Description:[/bold] {metadata.description}")
    if hasattr(metadata, "type") and metadata.type:
        console.print(f"[bold]Type:[/bold] {metadata.type}")
    if hasattr(metadata, "unit") and metadata.unit:
        console.print(f"[bold]Unit:[/bold] {metadata.unit}")
    if hasattr(metadata, "per_unit") and metadata.per_unit:
        console.print(f"[bold]Per Unit:[/bold] {metadata.per_unit}")
