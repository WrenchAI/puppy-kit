"""MCP server exposing Datadog operations as tools for AI agents.

Requires the 'mcp' optional dependency:
    pip install puppy-kit[mcp]

Run:
    python -m puppy_kit.mcp.server
"""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from puppy_kit.client import DatadogClient
from puppy_kit.config import load_config

mcp = FastMCP(
    "puppy-kit",
    instructions=(
        "Datadog operations for AI-driven incident lifecycle management. "
        "Detect, triage, document, and resolve incidents autonomously."
    ),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_client() -> DatadogClient:
    """Create a DatadogClient using env vars / config file (no Click context)."""
    config = load_config()
    return DatadogClient(config)


def _to_json(data: Any) -> str:  # noqa: ANN401
    """Serialize SDK response data to JSON string."""
    return json.dumps(data, indent=2, default=str)


def _extract_monitor(m: object) -> dict[str, Any]:
    """Extract key fields from a Datadog monitor SDK object."""
    return {
        "id": getattr(m, "id", None),
        "name": getattr(m, "name", ""),
        "type": str(getattr(m, "type", "")),
        "overall_state": str(getattr(m, "overall_state", "")),
        "query": getattr(m, "query", ""),
        "message": getattr(m, "message", ""),
        "tags": getattr(m, "tags", []),
    }


def _extract_incident(inc: object) -> dict[str, Any]:
    """Extract key fields from a Datadog incident SDK object."""
    attrs = getattr(inc, "attributes", inc)
    return {
        "id": getattr(inc, "id", None),
        "title": getattr(attrs, "title", ""),
        "status": str(getattr(attrs, "status", "")),
        "severity": str(getattr(attrs, "severity", "")),
        "created": str(getattr(attrs, "created", "")),
        "modified": str(getattr(attrs, "modified", "")),
    }


# ---------------------------------------------------------------------------
# Monitors
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_monitors_list(
    name: str | None = None,
    tags: str | None = None,
    page_size: int = 100,
) -> str:
    """List Datadog monitors with optional filtering.

    Args:
        name: Filter by monitor name substring.
        tags: Filter by monitor tags (comma-separated).
        page_size: Number of monitors per page.

    Returns JSON array of monitor summaries.
    """
    with _get_client() as client:
        kwargs: dict[str, Any] = {"page_size": page_size}
        if name:
            kwargs["name"] = name
        if tags:
            kwargs["monitor_tags"] = tags
        monitors = client.monitors.list_monitors(**kwargs)
    return _to_json([_extract_monitor(m) for m in monitors])


@mcp.tool()
def dd_monitors_get(monitor_id: int) -> str:
    """Get details of a specific Datadog monitor.

    Args:
        monitor_id: The monitor ID to retrieve.

    Returns JSON with monitor details including query, thresholds, status.
    """
    with _get_client() as client:
        m = client.monitors.get_monitor(monitor_id=monitor_id)
    return _to_json(_extract_monitor(m))


@mcp.tool()
def dd_monitors_create(
    name: str,
    monitor_type: str,
    query: str,
    message: str = "",
    tags: list[str] | None = None,
) -> str:
    """Create a new Datadog monitor.

    Args:
        name: Monitor name.
        monitor_type: Type (e.g. 'metric alert', 'log alert', 'service check').
        query: Monitor query string.
        message: Notification message (supports @slack-channel, @email).
        tags: Monitor tags.

    Returns JSON of the created monitor.
    """
    from datadog_api_client.v1.model.monitor import Monitor

    body = Monitor(
        name=name,
        type=monitor_type,
        query=query,
        message=message,
        tags=tags or [],
    )
    with _get_client() as client:
        result = client.monitors.create_monitor(body=body)
    return _to_json(_extract_monitor(result))


@mcp.tool()
def dd_monitors_delete(monitor_id: int) -> str:
    """Delete a Datadog monitor.

    Args:
        monitor_id: The monitor ID to delete.

    Returns confirmation message.
    """
    with _get_client() as client:
        client.monitors.delete_monitor(monitor_id=monitor_id)
    return _to_json({"status": "deleted", "monitor_id": monitor_id})


@mcp.tool()
def dd_monitors_mute(monitor_id: int) -> str:
    """Mute a Datadog monitor.

    Args:
        monitor_id: The monitor ID to mute.

    Returns JSON of the muted monitor.
    """
    with _get_client() as client:
        result = client.monitors.mute_monitor(monitor_id=monitor_id)
    return _to_json(_extract_monitor(result))


@mcp.tool()
def dd_monitors_unmute(monitor_id: int) -> str:
    """Unmute a Datadog monitor.

    Args:
        monitor_id: The monitor ID to unmute.

    Returns confirmation message.
    """
    with _get_client() as client:
        client.monitors.unmute_monitor(monitor_id=monitor_id)
    return _to_json({"status": "unmuted", "monitor_id": monitor_id})


# ---------------------------------------------------------------------------
# Incidents
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_incidents_list(page_size: int = 25) -> str:
    """List all Datadog incidents.

    Returns a JSON array of incident summaries with id, title, status, severity.
    """
    with _get_client() as client:
        response = client.incidents.list_incidents()
    incidents = response.data if response.data else []
    return _to_json([_extract_incident(inc) for inc in incidents[:page_size]])


@mcp.tool()
def dd_incidents_get(incident_id: str) -> str:
    """Get full details of a Datadog incident.

    Args:
        incident_id: The incident ID to retrieve.

    Returns JSON with id, title, status, severity, created, modified.
    """
    with _get_client() as client:
        response = client.incidents.get_incident(incident_id=incident_id)
    return _to_json(_extract_incident(response.data))


@mcp.tool()
def dd_incidents_create(
    title: str,
    customer_impacted: bool = False,
    severity: str | None = None,
) -> str:
    """Create a new Datadog incident.

    Args:
        title: Incident title describing the issue.
        customer_impacted: Whether customers are affected.
        severity: Severity level (e.g. SEV-1, SEV-2, SEV-3, SEV-4, SEV-5).

    Returns JSON of the created incident.
    """
    from datadog_api_client.v2.model.incident_create_attributes import (
        IncidentCreateAttributes,
    )
    from datadog_api_client.v2.model.incident_create_data import IncidentCreateData
    from datadog_api_client.v2.model.incident_create_request import (
        IncidentCreateRequest,
    )

    attrs_kwargs: dict[str, Any] = {
        "title": title,
        "customer_impacted": customer_impacted,
    }
    if severity:
        attrs_kwargs["fields"] = {
            "severity": {"type": "dropdown", "value": severity},
        }

    body = IncidentCreateRequest(
        data=IncidentCreateData(
            type="incidents",
            attributes=IncidentCreateAttributes(**attrs_kwargs),
        )
    )
    with _get_client() as client:
        response = client.incidents.create_incident(body=body)
    return _to_json(_extract_incident(response.data))


@mcp.tool()
def dd_incidents_update(
    incident_id: str,
    title: str | None = None,
    severity: str | None = None,
    status: str | None = None,
) -> str:
    """Update an existing Datadog incident.

    Args:
        incident_id: The incident ID to update.
        title: New title (optional).
        severity: New severity (optional).
        status: New status like 'active', 'stable', 'resolved' (optional).

    Returns JSON of the updated incident.
    """
    from datadog_api_client.v2.model.incident_update_attributes import (
        IncidentUpdateAttributes,
    )
    from datadog_api_client.v2.model.incident_update_data import IncidentUpdateData
    from datadog_api_client.v2.model.incident_update_request import (
        IncidentUpdateRequest,
    )

    attrs_kwargs: dict[str, Any] = {}
    if title is not None:
        attrs_kwargs["title"] = title
    if status is not None:
        attrs_kwargs["status"] = status
    if severity is not None:
        attrs_kwargs["fields"] = {
            "severity": {"type": "dropdown", "value": severity},
        }

    body = IncidentUpdateRequest(
        data=IncidentUpdateData(
            id=incident_id,
            type="incidents",
            attributes=IncidentUpdateAttributes(**attrs_kwargs),
        )
    )
    with _get_client() as client:
        response = client.incidents.update_incident(incident_id=incident_id, body=body)
    return _to_json(_extract_incident(response.data))


@mcp.tool()
def dd_incidents_delete(incident_id: str) -> str:
    """Delete a Datadog incident.

    Args:
        incident_id: The incident ID to delete.

    Returns confirmation message.
    """
    with _get_client() as client:
        client.incidents.delete_incident(incident_id=incident_id)
    return _to_json({"status": "deleted", "incident_id": incident_id})


# ---------------------------------------------------------------------------
# Downtimes
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_downtimes_list() -> str:
    """List all Datadog downtimes.

    Returns JSON array of downtime summaries.
    """
    with _get_client() as client:
        downtimes = client.downtimes.list_downtimes()
    results = []
    for dt in downtimes:
        results.append(
            {
                "id": getattr(dt, "id", None),
                "scope": getattr(dt, "scope", []),
                "message": getattr(dt, "message", ""),
                "monitor_id": getattr(dt, "monitor_id", None),
                "disabled": getattr(dt, "disabled", False),
            }
        )
    return _to_json(results)


@mcp.tool()
def dd_downtimes_create(
    scope: str,
    message: str = "",
    monitor_id: int | None = None,
) -> str:
    """Create a Datadog downtime (mute monitors).

    Args:
        scope: Downtime scope (e.g. 'env:production', 'host:web-01').
        message: Reason for the downtime.
        monitor_id: Specific monitor ID to mute (optional).

    Returns JSON of the created downtime.
    """
    from datadog_api_client.v1.model.downtime import Downtime

    body_kwargs: dict[str, Any] = {
        "scope": [scope],
        "message": message,
    }
    if monitor_id is not None:
        body_kwargs["monitor_id"] = monitor_id

    body = Downtime(**body_kwargs)
    with _get_client() as client:
        result = client.downtimes.create_downtime(body=body)
    return _to_json(
        {
            "id": getattr(result, "id", None),
            "scope": getattr(result, "scope", []),
            "message": getattr(result, "message", ""),
        }
    )


@mcp.tool()
def dd_downtimes_cancel(downtime_id: int) -> str:
    """Cancel a Datadog downtime.

    Args:
        downtime_id: The downtime ID to cancel.

    Returns confirmation message.
    """
    with _get_client() as client:
        client.downtimes.cancel_downtime(downtime_id=downtime_id)
    return _to_json({"status": "canceled", "downtime_id": downtime_id})


# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_logs_search(
    query: str,
    from_time: str = "now-15m",
    to_time: str = "now",
    limit: int = 25,
) -> str:
    """Search Datadog logs.

    Args:
        query: Log search query (Datadog syntax, e.g. 'service:api status:error').
        from_time: Start time (e.g. 'now-1h', 'now-15m').
        to_time: End time (e.g. 'now').
        limit: Maximum number of log entries to return (1-1000).

    Returns JSON array of log entries.
    """
    from datadog_api_client.v2.model.logs_list_request import LogsListRequest
    from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
    from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter

    body = LogsListRequest(
        filter=LogsQueryFilter(
            query=query,
            _from=from_time,
            to=to_time,
        ),
        page=LogsListRequestPage(limit=limit),
    )
    with _get_client() as client:
        response = client.logs.list_logs(body=body)

    logs = response.data if response.data else []
    results = []
    for log in logs:
        attrs = getattr(log, "attributes", log)
        results.append(
            {
                "id": getattr(log, "id", ""),
                "timestamp": str(getattr(attrs, "timestamp", "")),
                "service": getattr(attrs, "service", ""),
                "status": getattr(attrs, "status", ""),
                "message": getattr(attrs, "message", ""),
            }
        )
    return _to_json(results)


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

    Args:
        query: Metric query string (e.g. 'avg:system.cpu.idle{*}').
        from_time: Start time — relative like '1h', '30m', '7d' or epoch seconds.
        to_time: End time — 'now' or epoch seconds.

    Returns JSON with query metadata and time series data points.
    """
    from puppy_kit.utils.time import parse_time_range

    from_ts, to_ts = parse_time_range(from_time)
    if to_time != "now":
        to_ts = int(to_time)

    with _get_client() as client:
        result = client.metrics.query_metrics(
            _from=from_ts,
            to=to_ts,
            query=query,
        )
    series_list = getattr(result, "series", []) or []
    output = []
    for series in series_list:
        output.append(
            {
                "metric": getattr(series, "metric", ""),
                "scope": getattr(series, "scope", ""),
                "pointlist": [
                    {"timestamp": p[0], "value": p[1]}
                    for p in (getattr(series, "pointlist", []) or [])
                ],
            }
        )
    return _to_json({"query": query, "series": output})


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_events_create(
    title: str,
    text: str,
    tags: list[str] | None = None,
    alert_type: str = "info",
) -> str:
    """Create a Datadog event.

    Args:
        title: Event title.
        text: Event body (supports markdown).
        tags: Event tags.
        alert_type: One of 'info', 'warning', 'error', 'success'.

    Returns JSON of the created event.
    """
    from datadog_api_client.v1.model.event_create_request import EventCreateRequest

    body = EventCreateRequest(
        title=title,
        text=text,
        tags=tags or [],
        alert_type=alert_type,
    )
    with _get_client() as client:
        result = client.events.create_event(body=body)
    event = getattr(result, "event", result)
    return _to_json(
        {
            "id": getattr(event, "id", None),
            "title": getattr(event, "title", ""),
            "status": "created",
        }
    )


@mcp.tool()
def dd_events_search(
    query: str,
    from_time: str = "now-1h",
    to_time: str = "now",
    limit: int = 25,
) -> str:
    """Search Datadog events.

    Args:
        query: Event search query.
        from_time: Start time.
        to_time: End time.
        limit: Max results.

    Returns JSON array of event summaries.
    """
    from puppy_kit.utils.time import parse_time_range

    from_ts, to_ts = parse_time_range(from_time)
    if to_time != "now":
        to_ts = int(to_time)

    with _get_client() as client:
        result = client.events.list_events(
            start=from_ts,
            end=to_ts,
        )
    events = getattr(result, "events", []) or []
    output = []
    for ev in events[:limit]:
        output.append(
            {
                "id": getattr(ev, "id", None),
                "title": getattr(ev, "title", ""),
                "text": getattr(ev, "text", ""),
                "date_happened": str(getattr(ev, "date_happened", "")),
                "tags": getattr(ev, "tags", []),
            }
        )
    return _to_json(output)


# ---------------------------------------------------------------------------
# Dashboards
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_dashboards_list() -> str:
    """List all Datadog dashboards.

    Returns JSON array of dashboard summaries with id, title, layout_type.
    """
    with _get_client() as client:
        result = client.dashboards.list_dashboards()
    dashboards = getattr(result, "dashboards", []) or []
    output = []
    for d in dashboards:
        output.append(
            {
                "id": getattr(d, "id", ""),
                "title": getattr(d, "title", ""),
                "layout_type": str(getattr(d, "layout_type", "")),
            }
        )
    return _to_json(output)


@mcp.tool()
def dd_dashboards_get(dashboard_id: str) -> str:
    """Get full details of a Datadog dashboard.

    Args:
        dashboard_id: The dashboard ID to retrieve.

    Returns JSON with dashboard details.
    """
    with _get_client() as client:
        result = client.dashboards.get_dashboard(dashboard_id=dashboard_id)
    return _to_json(
        {
            "id": getattr(result, "id", ""),
            "title": getattr(result, "title", ""),
            "layout_type": str(getattr(result, "layout_type", "")),
            "widget_count": len(getattr(result, "widgets", []) or []),
            "description": getattr(result, "description", ""),
        }
    )


# ---------------------------------------------------------------------------
# Hosts
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_hosts_list(
    filter_query: str | None = None,
    count: int = 100,
) -> str:
    """List Datadog hosts.

    Args:
        filter_query: Filter query string (e.g. 'env:production').
        count: Number of hosts to return.

    Returns JSON array of host summaries.
    """
    kwargs: dict[str, Any] = {"count": count}
    if filter_query:
        kwargs["filter"] = filter_query

    with _get_client() as client:
        result = client.hosts.list_hosts(**kwargs)
    host_list = getattr(result, "host_list", []) or []
    output = []
    for h in host_list:
        output.append(
            {
                "name": getattr(h, "name", ""),
                "id": getattr(h, "id", None),
                "apps": getattr(h, "apps", []),
                "tags_by_source": getattr(h, "tags_by_source", {}),
            }
        )
    return _to_json(output)


# ---------------------------------------------------------------------------
# SLOs
# ---------------------------------------------------------------------------


@mcp.tool()
def dd_slos_list() -> str:
    """List all Datadog SLOs.

    Returns JSON array of SLO summaries.
    """
    with _get_client() as client:
        result = client.slos.list_slos()
    slos = getattr(result, "data", []) or []
    output = []
    for s in slos:
        output.append(
            {
                "id": getattr(s, "id", ""),
                "name": getattr(s, "name", ""),
                "type": str(getattr(s, "type", "")),
                "target_threshold": getattr(s, "target_threshold", None),
                "tags": getattr(s, "tags", []),
            }
        )
    return _to_json(output)


@mcp.tool()
def dd_slos_get(slo_id: str) -> str:
    """Get details of a specific Datadog SLO.

    Args:
        slo_id: The SLO ID to retrieve.

    Returns JSON with SLO details.
    """
    with _get_client() as client:
        result = client.slos.get_slo(slo_id=slo_id)
    slo = getattr(result, "data", result)
    return _to_json(
        {
            "id": getattr(slo, "id", ""),
            "name": getattr(slo, "name", ""),
            "type": str(getattr(slo, "type", "")),
            "description": getattr(slo, "description", ""),
            "target_threshold": getattr(slo, "target_threshold", None),
            "tags": getattr(slo, "tags", []),
        }
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
