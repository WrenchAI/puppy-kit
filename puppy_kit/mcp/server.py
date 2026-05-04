"""MCP server exposing Datadog operations as tools for AI agents.

Requires the 'mcp' optional dependency:
    pip install puppy-kit[mcp]

Run:
    python -m puppy_kit.mcp.server
"""

from __future__ import annotations

from click.testing import CliRunner
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "puppy-kit",
    instructions=(
        "Datadog operations for AI-driven incident lifecycle management. "
        "Detect, triage, document, and resolve incidents autonomously."
    ),
)


# ---------------------------------------------------------------------------
# Monitors
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_monitors_list(
    tags: str | None = None,
    page_size: int = 100,
) -> str:
    """List Datadog monitors with optional tag and state filters.

    Use this to survey monitor health, find monitors in Alert or Warn state, or
    locate a specific monitor by name before investigating. Returns id, name, type,
    overall_state, query, message, and tags for each monitor.

    Args:
        tags: Filter by monitor tags (comma-separated).
        page_size: Number of monitors to return.

    Returns JSON array of monitor summaries.
    """
    from puppy_kit.commands.monitor import list_monitors

    args = ["--format", "json", "--limit", str(page_size)]
    if tags:
        args += ["--tags", tags]
    result = CliRunner().invoke(list_monitors, args, catch_exceptions=False)
    return result.output


@mcp.tool()
def dd_monitors_get(monitor_id: int) -> str:
    """Get full configuration and current state of a single Datadog monitor by ID.

    Use this when you have a monitor ID and need its query, thresholds, notification
    message, or current alert status before deciding on a course of action.

    Args:
        monitor_id: The monitor ID to retrieve.

    Returns JSON with monitor details including query, thresholds, and overall_state.
    """
    from puppy_kit.commands.monitor import get_monitor

    result = CliRunner().invoke(
        get_monitor, [str(monitor_id), "--format", "json"], catch_exceptions=False
    )
    return result.output


# ---------------------------------------------------------------------------
# Incidents
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_incidents_list(
    status: str | None = None, page_size: int = 25, sort: str = "-created"
) -> str:
    """List Datadog incidents. This is the primary triage tool — call this first.

    Defaults to newest-first with no status filter (returns all). To see only open
    incidents pass status='active' or status='stable'. To see the current incident
    queue pass status='active' and status='stable' in two separate calls and merge.
    Returns id, title, status, severity, created, and modified for each incident.

    Args:
        status: Filter by status: 'active', 'stable', or 'resolved'. None returns all.
        page_size: Max incidents to return.
        sort: '-created' (newest first, default) or 'created' (oldest first).

    Returns JSON array of incident summaries.
    """
    from puppy_kit.commands.incident import list_incidents

    args = ["--format", "json", "--limit", str(page_size), "--sort", sort]
    if status:
        args += ["--status", status]
    result = CliRunner().invoke(list_incidents, args, catch_exceptions=False)
    return result.output


@mcp.tool()
def dd_incidents_get(incident_id: str) -> str:
    """Get full details of a single Datadog incident by ID.

    Use this after dd_incidents_list to drill into a specific incident. Returns
    title, status, severity, customer_impacted, public_id, detected, resolved,
    created, and modified timestamps.

    Args:
        incident_id: The incident UUID to retrieve.

    Returns JSON with full incident details.
    """
    from puppy_kit.commands.incident import get_incident

    result = CliRunner().invoke(
        get_incident, [incident_id, "--format", "json"], catch_exceptions=False
    )
    return result.output


@mcp.tool()
def dd_incidents_create(
    title: str,
    severity: str,
    team: str,
    customer_impacted: bool = False,
    assignee: str | None = None,
) -> str:
    """Create a new Datadog incident when a confirmed issue needs to be tracked.

    Use this when a new problem is detected and requires an incident record. Requires
    a descriptive title, severity, and owning team. Returns the created incident ID
    which can then be passed to dd_incidents_update to set status and add detail.

    Args:
        title: Short descriptive title of the issue.
        severity: SEV-1 (critical/outage) through SEV-5 (cosmetic/low impact).
        team: Team name responsible for this incident.
        customer_impacted: Set True if customers are experiencing impact.
        assignee: Assignee user UUID to set as incident commander (optional).

    Returns JSON of the created incident including its ID.
    """
    from puppy_kit.commands.incident import create_incident

    args = [
        "--format",
        "json",
        "--title",
        title,
        "--severity",
        severity,
        "--team",
        team,
    ]
    if assignee:
        args += ["--assignee", assignee]
    if customer_impacted:
        args.append("--customer-impacted")
    result = CliRunner().invoke(create_incident, args, catch_exceptions=False)
    return result.output


@mcp.tool()
def dd_incidents_update(
    incident_id: str,
    title: str | None = None,
    severity: str | None = None,
    status: str | None = None,
) -> str:
    """Update an existing Datadog incident's title, severity, or status.

    Use to progress an incident through its lifecycle. At least one field must be
    provided. Typical flow: create with status 'active', set 'stable' once contained,
    set 'resolved' once the fix is confirmed. To close an incident always use
    status='resolved' here — do not use dd_incidents_delete for real incidents.

    Args:
        incident_id: The incident UUID to update.
        title: New title (optional).
        severity: New severity — SEV-1 through SEV-5 (optional).
        status: 'active', 'stable', or 'resolved' (optional).

    Returns JSON of the updated incident.
    """
    from puppy_kit.commands.incident import update_incident

    args = ["--format", "json", incident_id]
    if title is not None:
        args += ["--title", title]
    if severity is not None:
        args += ["--severity", severity]
    if status is not None:
        args += ["--status", status]
    result = CliRunner().invoke(update_incident, args, catch_exceptions=False)
    return result.output


@mcp.tool()
def dd_incidents_delete(incident_id: str) -> str:
    """Permanently delete a Datadog incident. Use only to remove erroneous or duplicate records.

    This is irreversible. For closing a real incident, use dd_incidents_update with
    status='resolved' instead — that preserves the incident history. Only call this
    when an incident was created by mistake and should not exist at all.

    Args:
        incident_id: The incident UUID to delete.

    Returns confirmation message.
    """
    from puppy_kit.commands.incident import delete_incident

    result = CliRunner().invoke(delete_incident, [incident_id, "--confirm"], catch_exceptions=False)
    return result.output


# ---------------------------------------------------------------------------
# Downtimes
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_downtimes_list() -> str:
    """List all Datadog downtimes (scheduled monitor silences), both active and disabled.

    Use this before filing a false-positive incident to check whether the affected
    monitor or scope is already silenced, or before creating a new downtime to avoid
    duplicates. Returns id, scope, monitor_id, message, and disabled flag.

    Returns JSON array of downtime summaries.
    """
    from puppy_kit.commands.downtime import list_downtimes

    result = CliRunner().invoke(list_downtimes, ["--format", "json"], catch_exceptions=False)
    return result.output


@mcp.tool()
def dd_downtimes_cancel(downtime_id: int) -> str:
    """Cancel an active Datadog downtime so monitors resume alerting.

    Use when maintenance or a known outage window is complete and normal alerting
    should be restored. Retrieve the downtime ID first from dd_downtimes_list.

    Args:
        downtime_id: The downtime ID to cancel.

    Returns confirmation message.
    """
    from puppy_kit.commands.downtime import delete_downtime_cmd

    result = CliRunner().invoke(
        delete_downtime_cmd, [str(downtime_id), "--confirm"], catch_exceptions=False
    )
    return result.output


# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_logs_search(
    query: str,
    from_time: str = "15m",
    to_time: str = "now",
    limit: int = 25,
) -> str:
    """Search Datadog logs using Datadog query syntax.

    Use during incident investigation to find error patterns, stack traces, or service
    failures correlated with an incident timeline. Narrow the time window to the period
    of impact for the most relevant results. Defaults to the last 15 minutes.
    Example queries: 'service:api status:error', 'env:prod @http.status_code:500'.

    Args:
        query: Datadog log search query using facet syntax.
        from_time: Relative duration like '15m', '1h', or '7d', or an ISO timestamp.
        to_time: 'now', a relative duration, or an ISO timestamp.
        limit: Maximum log entries to return (1-1000).

    Returns JSON array of log entries with timestamp, service, status, and message.
    """
    from puppy_kit.commands.logs import search_logs

    args = [
        query,
        "--format",
        "json",
        "--from",
        from_time,
        "--to",
        to_time,
        "--limit",
        str(limit),
    ]
    result = CliRunner().invoke(search_logs, args, catch_exceptions=False)
    return result.output


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_metrics_query(
    query: str,
    from_time: str = "1h",
    to_time: str = "now",
) -> str:
    """Query Datadog metrics over a time range.

    Use during incident investigation to check CPU, memory, error rates, latency, or
    any custom metric that may explain the symptoms. Defaults to the last hour.
    Example queries: 'avg:system.cpu.user{env:prod}', 'sum:trace.web.request.errors{*}'.

    Args:
        query: Datadog metric query string.
        from_time: Relative duration like '1h', '30m', '7d', or an ISO timestamp.
        to_time: 'now', a relative duration, or an ISO timestamp.

    Returns JSON with query metadata and time series data points.
    """
    from puppy_kit.commands.metric import query_metric

    args = [
        query,
        "--format",
        "json",
        "--from",
        from_time,
        "--to",
        to_time,
    ]
    result = CliRunner().invoke(query_metric, args, catch_exceptions=False)
    return result.output


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_events_search(
    from_time: str = "1h",
    to_time: str = "now",
    limit: int = 25,
) -> str:
    """List Datadog events such as deploys, config changes, restarts, and alerts.

    Use during incident investigation to identify recent changes that may have triggered
    the issue — deployments, scaling events, or config pushes in the impact window are
    common root causes. Defaults to the last hour.

    Args:
        from_time: Relative duration like '1h', '30m', or '7d', or an ISO timestamp.
        to_time: 'now', a relative duration, or an ISO timestamp.
        limit: Max results to return.

    Returns JSON array of event summaries with title, text, date, and tags.
    """
    from puppy_kit.commands.event import list_events

    args = [
        "--format",
        "json",
        "--from",
        from_time,
        "--to",
        to_time,
        "--limit",
        str(limit),
    ]
    result = CliRunner().invoke(list_events, args, catch_exceptions=False)
    return result.output


# ---------------------------------------------------------------------------
# Dashboards
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_dashboards_list() -> str:
    """List all Datadog dashboards.

    Use to find a dashboard ID when you need to locate a relevant dashboard during
    an incident — e.g. a service health or infrastructure overview board. Pass the
    ID to dd_dashboards_get to retrieve its full details.

    Returns JSON array of dashboard summaries with id, title, and layout_type.
    """
    from puppy_kit.commands.dashboard import list_dashboards

    result = CliRunner().invoke(list_dashboards, ["--format", "json"], catch_exceptions=False)
    return result.output


@mcp.tool()
def dd_dashboards_get(dashboard_id: str) -> str:
    """Get full details of a Datadog dashboard by ID.

    Use to retrieve the dashboard title, description, and widget count — typically
    to confirm you have the right board before sharing it as incident context.
    Get the dashboard ID first from dd_dashboards_list.

    Args:
        dashboard_id: The dashboard ID to retrieve.

    Returns JSON with id, title, layout_type, description, and widget_count.
    """
    from puppy_kit.commands.dashboard import get_dashboard

    result = CliRunner().invoke(
        get_dashboard, [dashboard_id, "--format", "json"], catch_exceptions=False
    )
    return result.output


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
