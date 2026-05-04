"""LLM Observability commands."""

import click
import json
import warnings
from datetime import datetime
from typing import Any

import requests

from rich.console import Console
from rich.table import Table

from puppy_kit.client import get_datadog_client
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.format import json_list_response
from puppy_kit.utils.time import parse_time_range

warnings.filterwarnings("ignore", message=".*is unstable.*")

console = Console()


def _format_api_timestamp(ts: int) -> str:
    """Format a Unix timestamp for the Spans API in UTC without microseconds."""
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")  # ty:ignore[deprecated]


def _format_datetime(dt: Any) -> str:
    """Format datetime object or return N/A."""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"


def _any_to_str(value: Any) -> str:
    """Convert any value to a readable string."""
    if value is None:
        return "N/A"
    if isinstance(value, dict):
        return json.dumps(value, default=str)
    if isinstance(value, (list, tuple)):
        return str(value)
    return str(value)


def _truncate(value: Any, max_len: int = 60) -> str:
    """Convert a value to string and truncate it for table output."""
    text = _any_to_str(value)
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def _first_attr(obj: Any, *names: str) -> Any:
    """Return the first non-None attribute from an object."""
    for name in names:
        value = getattr(obj, name, None)
        if value is not None:
            return value
    return None


def _get_span_meta(attrs: Any) -> Any:
    """Return span metadata container if present."""
    return getattr(attrs, "meta", None) or getattr(attrs, "metadata", None)


def _get_nested_value(obj: Any, name: str) -> Any:
    """Read a field from an object or dict, including dotted keys and nested paths."""
    if obj is None:
        return None

    if isinstance(obj, dict):
        if obj.get(name) is not None:
            return obj.get(name)

        current = obj
        for part in name.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
            if current is None:
                return None
        return current

    value = getattr(obj, name, None)
    if value is not None:
        return value

    current = obj
    for part in name.split("."):
        current = getattr(current, part, None)
        if current is None:
            return None
    return current


def _get_span_field(span: Any, *names: str) -> Any:
    """Read a field from span attributes first, then metadata."""
    attrs = getattr(span, "attributes", None)
    if attrs:
        for name in names:
            value = _get_nested_value(attrs, name)
            if value is not None:
                return value

    meta = _get_span_meta(attrs) if attrs else None
    if meta:
        for name in names:
            value = _get_nested_value(meta, name)
            if value is not None:
                return value

    for name in names:
        value = _get_nested_value(span, name)
        if value is not None:
            return value
    return None


def _format_timestamp(value: Any) -> str | None:
    """Normalize datetime-like values to ISO8601 strings."""
    if isinstance(value, datetime):
        return value.isoformat()
    if value is None:
        return None
    return str(value)


def _serialize_value(value: Any) -> Any:
    """Convert API model objects to JSON-serializable values."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _serialize_value(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize_value(item) for item in value]
    if hasattr(value, "to_dict"):
        return _serialize_value(value.to_dict())
    if hasattr(value, "__dict__"):
        return {
            key: _serialize_value(val)
            for key, val in vars(value).items()
            if not key.startswith("_")
        }
    return value


def _get_duration_ms(span: Any) -> float:
    """Return span duration in milliseconds."""
    duration = _get_span_field(span, "duration")
    if duration is None:
        return 0.0
    return round(float(duration) / 1_000_000, 2)


def _format_llm_trace(span: Any) -> dict[str, Any]:
    """Extract common LLM trace fields from a span result."""
    attrs = getattr(span, "attributes", None)
    return {
        "span_id": _get_span_field(span, "span_id") or getattr(span, "id", None),
        "kind": _get_span_field(span, "span_kind", "kind"),
        "service": _get_span_field(span, "service"),
        "model": _get_span_field(span, "model", "model_name"),
        "provider": _get_span_field(span, "provider", "model_provider"),
        "operation": _get_span_field(
            span,
            "gen_ai.operation.name",
            "gen_ai_operation_name",
            "operation_name",
        ),
        "conversation_id": _get_span_field(
            span,
            "gen_ai.conversation.id",
            "gen_ai_conversation_id",
            "conversation_id",
        ),
        "duration": _get_duration_ms(span),
        "input": _get_span_field(
            span,
            "gen_ai.input",
            "gen_ai.request.input",
            "input",
        ),
        "output": _get_span_field(
            span,
            "gen_ai.output",
            "gen_ai.response.output",
            "output",
        ),
        "timestamp": _format_timestamp(
            _get_span_field(span, "start_timestamp", "timestamp", "start_time")
        ),
        "attributes": _serialize_value(getattr(attrs, "to_dict", lambda: attrs)()),
    }


@click.group()
def llm():
    """LLM Observability commands (projects, datasets, experiments, records)."""
    pass


@llm.command(name="traces")
@click.option("--ml-app", default=None, help="Filter by ML app name (e.g., ai-axis)")
@click.option(
    "--name", default=None, help="Filter by span name (e.g. FindEntityIdTool, BrandKitTool)"
)
@click.option(
    "--mode",
    type=click.Choice(["error", "irrelevant", "all"]),
    default="error",
    show_default=True,
    help=(
        "'error' = hard-failed spans (error:1); "
        "'irrelevant' = ToolNotRelevantException spans; "
        "'all' = no error filter"
    ),
)
@click.option(
    "--span-kind",
    type=click.Choice(["llm", "workflow", "agent", "tool", "task", "embedding", "retrieval"]),
    default=None,
    help="Filter by span kind (default: all kinds)",
)
@click.option("--model", default=None, help="Filter by model name (e.g., gpt-4o-mini)")
@click.option(
    "--from",
    "from_",
    default="1h",
    show_default=True,
    help="Time window: Nh (hours) or Nd (days), e.g. 1h, 24h, 2d",
)
@click.option(
    "--limit", type=int, default=None, help="Max traces to return (alias for --page-size)"
)
@click.option("--page-size", type=int, default=25, show_default=True)
@click.option("--verbose", is_flag=True, default=False, help="Show input/output messages")
@click.option(
    "--format", "fmt", type=click.Choice(["json", "table"]), default="table", show_default=True
)
@handle_api_error
def traces(
    ml_app: str | None,
    name: str | None,
    mode: str,
    span_kind: str | None,
    model: str | None,
    from_: str,
    limit: int | None,
    page_size: int,
    verbose: bool,
    fmt: str,
) -> None:
    """Query LLM Observability spans via the Export API (inputs, outputs, tokens, cost)."""
    client = get_datadog_client()

    # Use limit as alias for page_size if provided
    if limit is not None:
        page_size = limit

    # Parse time range to UTC ISO 8601
    from_ts, to_ts = parse_time_range(from_)
    from_iso = datetime.utcfromtimestamp(from_ts).strftime("%Y-%m-%dT%H:%M:%SZ")  # ty:ignore[deprecated]
    to_iso = datetime.utcfromtimestamp(to_ts).strftime("%Y-%m-%dT%H:%M:%SZ")  # ty:ignore[deprecated]

    # Build the LLM Obs Export API request body
    filter_block = {
        "from": from_iso,
        "to": to_iso,
    }

    if span_kind:
        filter_block["span_kind"] = span_kind

    if ml_app:
        filter_block["tags"] = {"ml_app": ml_app}  # ty:ignore[invalid-assignment]

    payload = {
        "data": {
            "type": "spans",
            "attributes": {
                "filter": filter_block,
                "page": {"limit": page_size},
                "sort": "timestamp",
            },
        }
    }

    # Get credentials and construct URL
    api_key = client.config.api_key
    app_key = client.config.app_key
    site = client.config.site

    url = f"https://api.{site}/api/v2/llm-obs/v1/spans/events/search"
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/vnd.api+json",
    }

    # Fetch spans via raw HTTP request
    with console.status("[cyan]Fetching LLM traces...[/cyan]"):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 403:
                raise click.ClickException(
                    "LLM Obs Export API returned 403 — check API key permissions"
                )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"API request failed: {e}")

        data = resp.json()

    # Extract and filter spans
    spans = data.get("data", [])

    # Apply name filter (client-side, case-insensitive substring match)
    if name:
        name_lower = name.lower()
        spans = [
            s for s in spans if name_lower in str(s.get("attributes", {}).get("name", "")).lower()
        ]

    # Apply mode filter (client-side)
    if mode == "error":
        # Filter to spans with status=error
        spans = [s for s in spans if s.get("attributes", {}).get("status") == "error"]
    elif mode == "irrelevant":
        # Filter to spans with ToolNotRelevantException
        spans = [
            s
            for s in spans
            if "ToolNotRelevantException" in str(s.get("attributes", {}).get("error_message", ""))
            or "ToolNotRelevantException"
            in str(s.get("attributes", {}).get("meta", {}).get("error", {}).get("type", ""))
        ]
    # mode == "all" -> no filter applied

    # Client-side filter by model if provided
    if model:
        model_lower = model.lower()
        spans = [
            s
            for s in spans
            if model_lower in str(s.get("attributes", {}).get("model_name", "")).lower()
        ]

    # Format spans for output
    output = []
    for span in spans:
        span_id = span.get("id", "N/A")
        attrs = span.get("attributes", {})

        metrics = attrs.get("metrics", {})
        duration_us = attrs.get("duration", 0)
        duration_ms = round(duration_us / 1_000_000, 2) if duration_us else 0.0

        formatted = {
            "span_id": span_id,
            "name": attrs.get("name", ""),
            "kind": attrs.get("span_kind", ""),
            "status": attrs.get("status", ""),
            "model": attrs.get("model_name", ""),
            "provider": attrs.get("model_provider", ""),
            "ml_app": attrs.get("ml_app", ""),
            "input_tokens": metrics.get("input_tokens", 0),
            "output_tokens": metrics.get("output_tokens", 0),
            "cost": metrics.get("estimated_total_cost", 0),
            "duration": duration_ms,
            "input": attrs.get("input", ""),
            "output": attrs.get("output", ""),
        }
        output.append(formatted)

    # Output as JSON or table
    if fmt == "json":
        # Remove input/output from JSON unless verbose
        if not verbose:
            output = [
                {k: v for k, v in item.items() if k not in ("input", "output")} for item in output
            ]
        click.echo(json.dumps(json_list_response(output), default=str))
    else:
        from rich.markup import escape

        table = Table(title="LLM Observability Spans")
        table.add_column("Name", style="cyan", min_width=22)
        table.add_column("Kind", style="white", width=10)
        table.add_column("Status", width=8)
        table.add_column("Model", style="dim", width=18)
        table.add_column("In Tok", justify="right", style="yellow", width=8)
        table.add_column("Out Tok", justify="right", style="yellow", width=8)
        table.add_column("Duration", justify="right", style="white", width=10)
        if verbose:
            table.add_column("Input", style="white", width=60)
            table.add_column("Output", style="white", width=60)

        for item in output:
            status = item["status"]
            status_str = f"[red]{status}[/red]" if status == "error" else escape(status)
            row_data = [
                escape(_truncate(item["name"], 26)),
                escape(_truncate(item["kind"], 10)),
                status_str,
                escape(_truncate(item["model"], 18)),
                str(item["input_tokens"]) if item["input_tokens"] else "",
                str(item["output_tokens"]) if item["output_tokens"] else "",
                f"{item['duration']:.0f}ms" if item["duration"] else "-",
            ]
            if verbose:
                row_data.extend(
                    [
                        escape(_truncate(item["input"], 200)),
                        escape(_truncate(item["output"], 200)),
                    ]
                )
            table.add_row(*row_data)

        console.print(table)
        console.print(f"\n[dim]Total traces: {len(output)}[/dim]")


@llm.command(name="projects")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@click.option("--page-size", type=int, default=25, help="Results per page")
@handle_api_error
def projects(format: str, page_size: int) -> None:
    """List LLM Observability projects.

    Query all projects sorted by creation date, newest first.
    """
    client = get_datadog_client()

    with console.status("[cyan]Fetching LLM projects...[/cyan]"):
        response = client.llm_observability.list_llm_obs_projects(page_limit=page_size)

    items = response.data if response and response.data else []

    if format == "json":
        output = []
        for item in items:
            obj = {
                "id": getattr(item, "id", None),
                "type": getattr(item, "type", None),
            }
            if hasattr(item, "attributes") and item.attributes:
                attrs = item.attributes
                obj["name"] = getattr(attrs, "name", None)
                obj["description"] = getattr(attrs, "description", None)
                obj["created_at"] = getattr(attrs, "created_at", None)
                obj["updated_at"] = getattr(attrs, "updated_at", None)
            output.append(obj)
        click.echo(json.dumps(json_list_response(output), default=str))
    else:
        table = Table(title="LLM Observability Projects")
        table.add_column("ID", style="cyan", width=20)
        table.add_column("Name", style="white", min_width=20)
        table.add_column("Created At", style="dim", width=20)

        for item in items:
            item_id = getattr(item, "id", "N/A")
            if len(str(item_id)) > 18:
                item_id = str(item_id)[:16] + ".."

            attrs = getattr(item, "attributes", None)
            if attrs:
                name = getattr(attrs, "name", "N/A")
                created_at = _format_datetime(getattr(attrs, "created_at", None))
            else:
                name = "N/A"
                created_at = "N/A"

            table.add_row(str(item_id), str(name), created_at)

        console.print(table)
        console.print(f"\n[dim]Total projects: {len(items)}[/dim]")


@llm.command(name="datasets")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@click.option("--page-size", type=int, default=25, help="Results per page")
@handle_api_error
def datasets(format: str, page_size: int) -> None:
    """List LLM Observability datasets.

    Query all datasets in the workspace.
    Note: Datasets are organized by project. This lists all datasets across projects.
    """
    client = get_datadog_client()

    with console.status("[cyan]Fetching LLM datasets...[/cyan]"):
        projects_resp = client.llm_observability.list_llm_obs_projects(page_limit=100)
        projects = projects_resp.data if projects_resp and projects_resp.data else []

    all_datasets = []
    with console.status("[cyan]Fetching datasets for each project...[/cyan]"):
        for project in projects:
            project_id = getattr(project, "id", None)
            if not project_id:
                continue
            try:
                ds_resp = client.llm_observability.list_llm_obs_datasets(
                    project_id=project_id, page_limit=page_size
                )
                if ds_resp and ds_resp.data:
                    all_datasets.extend(ds_resp.data)
            except Exception:
                pass

    if format == "json":
        output = []
        for item in all_datasets:
            obj = {
                "id": getattr(item, "id", None),
                "type": getattr(item, "type", None),
            }
            if hasattr(item, "attributes") and item.attributes:
                attrs = item.attributes
                obj["name"] = getattr(attrs, "name", None)
                obj["description"] = getattr(attrs, "description", None)
                obj["created_at"] = getattr(attrs, "created_at", None)
                obj["current_version"] = getattr(attrs, "current_version", None)
            output.append(obj)
        click.echo(json.dumps(json_list_response(output), default=str))
    else:
        table = Table(title="LLM Observability Datasets")
        table.add_column("ID", style="cyan", width=20)
        table.add_column("Name", style="white", min_width=20)
        table.add_column("Description", style="dim", width=25)
        table.add_column("Version", justify="right", width=10)

        for item in all_datasets:
            item_id = getattr(item, "id", "N/A")
            if len(str(item_id)) > 18:
                item_id = str(item_id)[:16] + ".."

            attrs = getattr(item, "attributes", None)
            if attrs:
                name = getattr(attrs, "name", "N/A")
                description = getattr(attrs, "description", None) or ""
                version = getattr(attrs, "current_version", "N/A")
            else:
                name = "N/A"
                description = ""
                version = "N/A"

            if len(str(description)) > 23:
                description = str(description)[:20] + "..."

            table.add_row(str(item_id), str(name), str(description), str(version))

        console.print(table)
        console.print(f"\n[dim]Total datasets: {len(all_datasets)}[/dim]")


@llm.command(name="experiments")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@click.option("--page-size", type=int, default=25, help="Results per page")
@handle_api_error
def experiments(format: str, page_size: int) -> None:
    """List LLM Observability experiments.

    Query all experiments sorted by creation date, newest first.
    """
    client = get_datadog_client()

    with console.status("[cyan]Fetching LLM experiments...[/cyan]"):
        response = client.llm_observability.list_llm_obs_experiments(page_limit=page_size)

    items = response.data if response and response.data else []

    if format == "json":
        output = []
        for item in items:
            obj = {
                "id": getattr(item, "id", None),
                "type": getattr(item, "type", None),
            }
            if hasattr(item, "attributes") and item.attributes:
                attrs = item.attributes
                obj["name"] = getattr(attrs, "name", None)
                obj["description"] = getattr(attrs, "description", None)
                obj["project_id"] = getattr(attrs, "project_id", None)
                obj["dataset_id"] = getattr(attrs, "dataset_id", None)
                obj["created_at"] = getattr(attrs, "created_at", None)
                obj["updated_at"] = getattr(attrs, "updated_at", None)
            output.append(obj)
        click.echo(json.dumps(json_list_response(output), default=str))
    else:
        table = Table(title="LLM Observability Experiments")
        table.add_column("ID", style="cyan", width=20)
        table.add_column("Name", style="white", min_width=20)
        table.add_column("Dataset ID", style="dim", width=18)
        table.add_column("Created At", width=20)

        for item in items:
            item_id = getattr(item, "id", "N/A")
            if len(str(item_id)) > 18:
                item_id = str(item_id)[:16] + ".."

            attrs = getattr(item, "attributes", None)
            if attrs:
                name = getattr(attrs, "name", "N/A")
                dataset_id = getattr(attrs, "dataset_id", "N/A")
                created_at = _format_datetime(getattr(attrs, "created_at", None))
            else:
                name = "N/A"
                dataset_id = "N/A"
                created_at = "N/A"

            if len(str(dataset_id)) > 16:
                dataset_id = str(dataset_id)[:14] + ".."

            table.add_row(str(item_id), str(name), str(dataset_id), created_at)

        console.print(table)
        console.print(f"\n[dim]Total experiments: {len(items)}[/dim]")


@llm.command(name="records")
@click.argument("dataset_id")
@click.option("--project-id", default=None, help="Project ID (required for datasets)")
@click.option("--format", type=click.Choice(["json", "table"]), default="table")
@click.option("--page-size", type=int, default=25, help="Results per page")
@handle_api_error
def records(dataset_id: str, project_id: str | None, format: str, page_size: int) -> None:
    """List records in an LLM Observability dataset.

    Args:
        DATASET_ID: The dataset ID to list records from
    """
    client = get_datadog_client()

    if not project_id:
        with console.status("[cyan]Discovering project for dataset...[/cyan]"):
            projects_resp = client.llm_observability.list_llm_obs_projects(page_limit=100)
            projects = projects_resp.data if projects_resp and projects_resp.data else []

            for project in projects:
                proj_id = getattr(project, "id", None)
                if not proj_id:
                    continue
                try:
                    ds_resp = client.llm_observability.list_llm_obs_datasets(
                        project_id=proj_id, page_limit=100
                    )
                    if ds_resp and ds_resp.data:
                        for ds in ds_resp.data:
                            if getattr(ds, "id", None) == dataset_id:
                                project_id = proj_id
                                break
                    if project_id:
                        break
                except Exception:
                    continue

    if not project_id:
        console.print("[red]Error: Could not find project for dataset.[/red]")
        console.print("[yellow]Tip: Use --project-id to specify the project explicitly.[/yellow]")
        return

    with console.status(f"[cyan]Fetching records from dataset {dataset_id}...[/cyan]"):
        response = client.llm_observability.list_llm_obs_dataset_records(
            project_id=project_id, dataset_id=dataset_id, page_limit=page_size
        )

    items = response.data if response and response.data else []

    if format == "json":
        output = []
        for item in items:
            obj = {
                "id": getattr(item, "id", None),
                "dataset_id": getattr(item, "dataset_id", None),
                "created_at": getattr(item, "created_at", None),
                "updated_at": getattr(item, "updated_at", None),
                "input": _any_to_str(getattr(item, "input", None)),
                "expected_output": _any_to_str(getattr(item, "expected_output", None)),
                "metadata": getattr(item, "metadata", None),
            }
            output.append(obj)
        click.echo(json.dumps(json_list_response(output), default=str))
    else:
        table = Table(title=f"Dataset Records: {dataset_id}")
        table.add_column("ID", style="cyan", width=18)
        table.add_column("Input", style="white", min_width=20)
        table.add_column("Expected Output", style="dim", width=20)
        table.add_column("Created At", width=20)

        for item in items:
            item_id = getattr(item, "id", "N/A")
            if len(str(item_id)) > 16:
                item_id = str(item_id)[:14] + ".."

            input_val = getattr(item, "input", None)
            input_str = _any_to_str(input_val)
            if len(input_str) > 18:
                input_str = input_str[:15] + "..."

            expected_output = getattr(item, "expected_output", None)
            expected_str = _any_to_str(expected_output)
            if len(expected_str) > 18:
                expected_str = expected_str[:15] + "..."

            created_at = _format_datetime(getattr(item, "created_at", None))

            table.add_row(str(item_id), input_str, expected_str, created_at)

        console.print(table)
        console.print(f"\n[dim]Total records: {len(items)}[/dim]")
