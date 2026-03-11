"""Billing and cost visibility commands."""

import calendar
import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from types import SimpleNamespace
from typing import cast

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from puppy_kit.client import DatadogClient, get_datadog_client
from puppy_kit.utils.error import handle_api_error
from puppy_kit.utils.format import json_list_response

console = Console()


@dataclass
class ProductCost:
    """Aggregated cost details for a single Datadog product."""

    product_name: str
    cost: float = 0.0
    usage_summaries: list[str] = field(default_factory=list)
    charge_types: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Delta:
    """Absolute and percentage delta between two values."""

    amount: float
    percent: float | None


def _to_namespace(value: object) -> object:
    """Convert decoded JSON dictionaries into namespaces for defensive getattr access."""
    if isinstance(value, dict):
        return SimpleNamespace(**{str(key): _to_namespace(item) for key, item in value.items()})
    if isinstance(value, list):
        return [_to_namespace(item) for item in value]
    return value


def _call_billing_api(
    client: DatadogClient,
    path: str,
    month: date | None = None,
) -> SimpleNamespace:
    """Call a billing endpoint through the raw SDK API client."""
    query_params: dict[str, str] = {}
    if month is not None:
        query_params["month"] = month.strftime("%Y-%m")

    api_client = getattr(client, "api_client", None)
    if api_client is None:
        raise RuntimeError("Datadog API client is not configured for raw billing calls.")
    response = api_client.call_api(
        path,
        "GET",
        query_params=query_params,
        header_params={"Accept": "application/json"},
    )
    raw_response = getattr(response, "response", None)
    raw_body = getattr(raw_response, "data", b"")

    if isinstance(raw_body, bytes):
        payload_text = raw_body.decode("utf-8")
    elif raw_body:
        payload_text = str(raw_body)
    else:
        payload_text = "{}"

    payload_object = cast(object, json.loads(payload_text) if payload_text else {})
    payload_namespace = _to_namespace(payload_object)
    if isinstance(payload_namespace, SimpleNamespace):
        return payload_namespace
    return SimpleNamespace(data=[], meta=SimpleNamespace())


def _coerce_float(value: object) -> float:
    """Convert numbers or numeric strings into floats, defaulting to zero."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0.0
    return 0.0


def _format_currency(value: float) -> str:
    """Format a cost value as USD."""
    return f"${value:,.2f}"


def _calculate_delta(current: float, previous: float) -> Delta:
    """Calculate absolute and percentage change with zero-safe division."""
    amount = current - previous
    if previous == 0:
        if current == 0:
            return Delta(amount=0.0, percent=0.0)
        return Delta(amount=amount, percent=None)
    return Delta(amount=amount, percent=(amount / previous) * 100.0)


def _month_start(target_date: date) -> date:
    """Return the first day of the month for the provided date."""
    return date(target_date.year, target_date.month, 1)


def _days_in_month(target_date: date) -> int:
    """Return the number of days in the month for the provided date."""
    return calendar.monthrange(target_date.year, target_date.month)[1]


def _format_usage(value: object) -> str:
    """Render usage summary values safely."""
    if value is None:
        return "-"
    if isinstance(value, SimpleNamespace):
        return json.dumps(vars(value), sort_keys=True, default=str)
    if isinstance(value, list):
        return ", ".join(_format_usage(item) for item in value) or "-"
    text = str(value).strip()
    return text or "-"


def _collect_product_costs(payload: SimpleNamespace) -> dict[str, ProductCost]:
    """Aggregate charge entries by product name."""
    aggregated: dict[str, ProductCost] = {}
    data_items = getattr(payload, "data", [])
    if not isinstance(data_items, list):
        return aggregated

    for data_item in data_items:
        attributes = getattr(data_item, "attributes", SimpleNamespace())
        charges = getattr(attributes, "charges", [])
        if not isinstance(charges, list):
            continue

        for charge in charges:
            product_name_raw = getattr(charge, "product_name", None)
            product_name = str(product_name_raw).strip() if product_name_raw else "Unknown"
            entry = aggregated.setdefault(product_name, ProductCost(product_name=product_name))

            entry.cost += _coerce_float(getattr(charge, "cost", 0.0))

            usage_summary = _format_usage(getattr(charge, "chargeable_usage_summary", None))
            if usage_summary != "-" and usage_summary not in entry.usage_summaries:
                entry.usage_summaries.append(usage_summary)

            charge_type_raw = getattr(charge, "charge_type", None)
            charge_type = str(charge_type_raw).strip() if charge_type_raw else ""
            if charge_type and charge_type not in entry.charge_types:
                entry.charge_types.append(charge_type)

    return aggregated


def _usage_label(product_cost: ProductCost) -> str:
    """Build a compact usage label for a product row."""
    if product_cost.usage_summaries:
        return "; ".join(product_cost.usage_summaries)
    if product_cost.charge_types:
        return ", ".join(product_cost.charge_types)
    return "-"


def _delta_text(delta: Delta, *, increase_threshold_percent: float | None = None) -> Text:
    """Format delta values with semantic color styling."""
    if delta.amount == 0:
        return Text(_format_currency(delta.amount), style="dim")

    if delta.amount < 0:
        return Text(_format_currency(delta.amount), style="green")

    if increase_threshold_percent is None:
        return Text(_format_currency(delta.amount), style="red")

    if delta.percent is None or delta.percent > increase_threshold_percent:
        return Text(_format_currency(delta.amount), style="red")
    return Text(_format_currency(delta.amount), style="yellow")


def _percent_text(delta: Delta, *, increase_threshold_percent: float | None = None) -> Text:
    """Format percentage deltas with semantic color styling."""
    if delta.percent is None:
        return Text("n/a", style="dim")
    if delta.percent == 0:
        return Text("0.0%", style="dim")
    if delta.percent < 0:
        return Text(f"{delta.percent:.1f}%", style="green")
    if increase_threshold_percent is None:
        return Text(f"+{delta.percent:.1f}%", style="red")
    if delta.percent > increase_threshold_percent:
        return Text(f"+{delta.percent:.1f}%", style="red")
    return Text(f"+{delta.percent:.1f}%", style="yellow")


def _sort_summary_rows(
    rows: list[dict[str, object]],
    sort_by: str,
) -> list[dict[str, object]]:
    """Sort summary rows according to the requested ordering."""
    if sort_by == "name":
        return sorted(rows, key=lambda row: str(row["product"]).lower())
    if sort_by == "cost":
        return sorted(rows, key=lambda row: _coerce_float(row["estimated_cost"]))
    return sorted(rows, key=lambda row: _coerce_float(row["estimated_cost"]), reverse=True)


@click.group()
def cost() -> None:
    """Datadog billing and cost visibility commands."""
    pass


@cost.command(name="summary")
@click.option("--format", "output_format", type=click.Choice(["json", "table"]), default="table")
@click.option("--all", "show_all", is_flag=True, help="Include products with zero estimated spend.")
@click.option(
    "--sort",
    "sort_by",
    type=click.Choice(["name", "cost", "-cost"]),
    default="-cost",
    help="Sort products by name or estimated cost.",
)
@handle_api_error
def summary(output_format: str, show_all: bool, sort_by: str) -> None:
    """Show current month estimated cost by product."""
    client = get_datadog_client()
    today = date.today()
    current_month = _month_start(today)
    previous_month = _month_start(_month_start(today) - timedelta(days=1))
    days_elapsed = max(today.day, 1)
    days_in_month = _days_in_month(today)

    with console.status("[cyan]Fetching estimated cost data...[/cyan]"):
        estimated_payload = _call_billing_api(client, "/api/v1/org/estimated_cost")
        previous_payload = _call_billing_api(
            client, "/api/v1/org/monthly_cost", month=previous_month
        )

    estimated_costs = _collect_product_costs(estimated_payload)
    previous_costs = _collect_product_costs(previous_payload)

    if not estimated_costs and not previous_costs:
        console.print("[dim]No cost data available.[/dim]")
        return

    product_names = set(estimated_costs)
    if show_all:
        product_names.update(previous_costs)

    rows: list[dict[str, object]] = []
    for product_name in sorted(product_names):
        current_entry = estimated_costs.get(product_name, ProductCost(product_name=product_name))
        previous_entry = previous_costs.get(product_name, ProductCost(product_name=product_name))
        projected_cost = (current_entry.cost / float(days_elapsed)) * float(days_in_month)
        delta = _calculate_delta(projected_cost, previous_entry.cost)

        if not show_all and current_entry.cost == 0:
            continue

        rows.append(
            {
                "product": product_name,
                "usage": _usage_label(current_entry),
                "estimated_cost": round(current_entry.cost, 2),
                "projected_end_of_month_cost": round(projected_cost, 2),
                "previous_month_cost": round(previous_entry.cost, 2),
                "delta_cost": round(delta.amount, 2),
                "delta_percent": None if delta.percent is None else round(delta.percent, 2),
                "charge_types": list(current_entry.charge_types),
            }
        )

    if not rows:
        console.print("[dim]No cost data available.[/dim]")
        return

    rows = _sort_summary_rows(rows, sort_by)

    if output_format == "json":
        output = {
            "current_month": current_month.isoformat(),
            "previous_month": previous_month.isoformat(),
            "generated_on": today.isoformat(),
            "days_elapsed": days_elapsed,
            "days_in_month": days_in_month,
            "sort": sort_by,
            "include_zero_spend": show_all,
            "estimated_meta": vars(getattr(estimated_payload, "meta", SimpleNamespace())),
            "previous_meta": vars(getattr(previous_payload, "meta", SimpleNamespace())),
            "rows": rows,
        }
        click.echo(json.dumps(json_list_response(output)))
        return

    table = Table(title=f"Estimated Cost Summary ({current_month.isoformat()})")
    table.add_column("Product", style="cyan")
    table.add_column("Usage", style="white")
    table.add_column("Est. Cost", justify="right", style="yellow")
    table.add_column("Proj. EOM", justify="right", style="yellow")
    table.add_column("$ Change", justify="right")
    table.add_column("% Change", justify="right")

    for row in rows:
        delta = _calculate_delta(
            _coerce_float(row["projected_end_of_month_cost"]),
            _coerce_float(row["previous_month_cost"]),
        )
        table.add_row(
            str(row["product"]),
            str(row["usage"]),
            _format_currency(_coerce_float(row["estimated_cost"])),
            _format_currency(_coerce_float(row["projected_end_of_month_cost"])),
            _delta_text(delta),
            _percent_text(delta),
        )

    console.print(table)
    console.print(
        f"[dim]Compared projected {current_month.isoformat()} costs against {previous_month.isoformat()} actuals.[/dim]"
    )


@cost.command(name="mom")
@click.option("--format", "output_format", type=click.Choice(["json", "table"]), default="table")
@click.option(
    "--threshold",
    type=float,
    default=1.0,
    show_default=True,
    help="Only show products with absolute change above this dollar amount.",
)
@click.option("--all", "show_all", is_flag=True, help="Include all products regardless of change.")
@handle_api_error
def month_over_month(output_format: str, threshold: float, show_all: bool) -> None:
    """Show month-over-month cost changes by product."""
    client = get_datadog_client()
    today = date.today()
    current_month = _month_start(today)
    previous_month = _month_start(current_month - timedelta(days=1))

    with console.status("[cyan]Fetching monthly cost data...[/cyan]"):
        current_payload = _call_billing_api(client, "/api/v1/org/monthly_cost", month=current_month)
        previous_payload = _call_billing_api(
            client, "/api/v1/org/monthly_cost", month=previous_month
        )

    current_costs = _collect_product_costs(current_payload)
    previous_costs = _collect_product_costs(previous_payload)

    if not current_costs and not previous_costs:
        console.print("[dim]No cost data available.[/dim]")
        return

    rows: list[dict[str, object]] = []
    for product_name in sorted(set(current_costs) | set(previous_costs)):
        current_entry = current_costs.get(product_name, ProductCost(product_name=product_name))
        previous_entry = previous_costs.get(product_name, ProductCost(product_name=product_name))
        delta = _calculate_delta(current_entry.cost, previous_entry.cost)

        if not show_all and abs(delta.amount) <= threshold:
            continue

        rows.append(
            {
                "product": product_name,
                "last_month_cost": round(previous_entry.cost, 2),
                "this_month_cost": round(current_entry.cost, 2),
                "delta_cost": round(delta.amount, 2),
                "delta_percent": None if delta.percent is None else round(delta.percent, 2),
                "usage": _usage_label(current_entry if current_entry.cost != 0 else previous_entry),
                "charge_types": list(
                    current_entry.charge_types
                    if current_entry.charge_types
                    else previous_entry.charge_types
                ),
            }
        )

    rows = sorted(rows, key=lambda row: abs(_coerce_float(row["delta_cost"])), reverse=True)

    if not rows:
        console.print(
            f"[dim]No significant changes above {_format_currency(threshold)} between "
            f"{previous_month.isoformat()} and {current_month.isoformat()}.[/dim]"
        )
        return

    if output_format == "json":
        output = {
            "current_month": current_month.isoformat(),
            "previous_month": previous_month.isoformat(),
            "threshold": threshold,
            "include_all": show_all,
            "current_meta": vars(getattr(current_payload, "meta", SimpleNamespace())),
            "previous_meta": vars(getattr(previous_payload, "meta", SimpleNamespace())),
            "rows": rows,
        }
        click.echo(json.dumps(json_list_response(output)))
        return

    table = Table(
        title=f"Month-over-Month Cost ({previous_month.isoformat()} -> {current_month.isoformat()})"
    )
    table.add_column("Product", style="cyan")
    table.add_column("Last Month", justify="right", style="yellow")
    table.add_column("This Month", justify="right", style="yellow")
    table.add_column("$ Change", justify="right")
    table.add_column("% Change", justify="right")

    for row in rows:
        delta = Delta(
            amount=_coerce_float(row["delta_cost"]),
            percent=cast(float | None, row["delta_percent"]),
        )
        table.add_row(
            str(row["product"]),
            _format_currency(_coerce_float(row["last_month_cost"])),
            _format_currency(_coerce_float(row["this_month_cost"])),
            _delta_text(delta, increase_threshold_percent=20.0),
            _percent_text(delta, increase_threshold_percent=20.0),
        )

    console.print(table)
