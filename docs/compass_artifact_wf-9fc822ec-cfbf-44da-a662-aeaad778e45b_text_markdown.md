# Fetching Datadog LLM traces via the Export API

**Datadog stores LLM Observability spans in a separate data store from APM**, which is why the standard APM traces API won't return your LLM data. The dedicated **LLM Observability Export API** — not documented alongside the main API reference but tucked under the Evaluations section — provides two endpoints for programmatically retrieving LLM spans. The `datadog-api-client` Python SDK does not wrap these endpoints, so you'll need raw HTTP calls via `requests` instead.

## LLM Observability lives outside APM

LLM Observability is a distinct Datadog product with its own Trace Explorer at `app.datadoghq.com/llm`. While both products share the underlying `ddtrace` library, their data flows into separate backends. This explains the confusion: querying `/api/v2/spans/events/search` (the APM Spans API) returns APM-side spans without LLM-specific fields like input messages, output completions, token counts, or evaluation results.

That said, the two systems are **correlatable**. When running LLM Observability through the Datadog Agent (non-agentless mode), APM spans are generated alongside LLM spans. The Datadog UI provides bidirectional navigation between them. But for programmatic access to the rich LLM data — inputs, outputs, model metadata, token metrics — you must use the Export API.

## Two endpoints for reading LLM spans

The Export API provides a **GET endpoint** for simple listing and a **POST endpoint** for filtered search. Both require an API key and an Application key.

**List spans** (simple, filter by trace ID):
```
GET https://api.datadoghq.com/api/v2/llm-obs/v1/spans/events
```

**Search spans** (rich filtering):
```
POST https://api.datadoghq.com/api/v2/llm-obs/v1/spans/events/search
```

Both return paginated results and default to the **past 15 minutes** if no time range is specified. There is no separate "traces" endpoint — a trace is simply the collection of spans sharing the same `trace_id`, so you reconstruct traces by filtering spans on that field.

### Available filter parameters for the search endpoint

The POST search endpoint accepts a JSON body with these filter options:

- **`from` / `to`** — ISO 8601 timestamps defining the time window
- **`trace_id`** — filter all spans belonging to a specific trace
- **`span_id`** — retrieve a single specific span
- **`span_kind`** — one of `llm`, `workflow`, `agent`, `tool`, `task`, `embedding`, `retrieval`
- **`tags`** — key-value pairs matching custom tags set during instrumentation
- **`page.limit`** — pagination control
- **`sort`** — sort field (e.g., `timestamp`)
- **`options.time_offset`** — time offset in seconds

## Python code for fetching LLM spans

Since `datadog-api-client` has **no `LLMObservabilityApi` class**, use `requests` directly. Here's a complete working example:

```python
import requests

DD_API_KEY = "<YOUR_DATADOG_API_KEY>"
DD_APP_KEY = "<YOUR_DATADOG_APPLICATION_KEY>"
DD_SITE = "datadoghq.com"  # or datadoghq.eu, us3.datadoghq.com, etc.

headers = {
    "DD-API-KEY": DD_API_KEY,
    "DD-APPLICATION-KEY": DD_APP_KEY,
    "Content-Type": "application/vnd.api+json",
}

# Search for all LLM-kind spans in a time window
payload = {
    "data": {
        "type": "spans",
        "attributes": {
            "filter": {
                "from": "2026-03-10T00:00:00Z",
                "to": "2026-03-11T23:59:59Z",
                "span_kind": "llm",
            },
            "page": {"limit": 50},
            "sort": "timestamp",
        },
    }
}

response = requests.post(
    f"https://api.{DD_SITE}/api/v2/llm-obs/v1/spans/events/search",
    headers=headers,
    json=payload,
)
data = response.json()

for span in data.get("data", []):
    attrs = span["attributes"]
    print(f"Span: {attrs['name']}")
    print(f"  Model: {attrs.get('model_name')} ({attrs.get('model_provider')})")
    print(f"  Tokens: {attrs.get('metrics', {}).get('total_tokens')}")
    print(f"  Input: {attrs.get('input', {}).get('value', '')[:100]}")
    print(f"  Output: {attrs.get('output', {}).get('value', '')[:100]}")
    print()
```

To **filter by custom tags** (set during instrumentation with `LLMObs.annotate(tags={...})`):

```python
payload = {
    "data": {
        "type": "spans",
        "attributes": {
            "filter": {
                "from": "2026-03-10T00:00:00Z",
                "to": "2026-03-11T23:59:59Z",
                "tags": {"environment": "production", "team": "ml-platform"},
            },
            "page": {"limit": 25},
        },
    }
}
```

To **retrieve all spans for a specific trace** using the simpler GET endpoint:

```python
trace_id = "6903738200000000af2d3775dfc70530"
response = requests.get(
    f"https://api.{DD_SITE}/api/v2/llm-obs/v1/spans/events",
    headers={
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
    },
    params={"filter[trace_id]": trace_id},
)
spans = response.json()["data"]
```

### Handling pagination for large result sets

Results are cursor-paginated. Iterate through pages like this:

```python
all_spans = []
payload = {
    "data": {
        "type": "spans",
        "attributes": {
            "filter": {
                "from": "2026-03-01T00:00:00Z",
                "to": "2026-03-11T00:00:00Z",
                "span_kind": "llm",
            },
            "page": {"limit": 100},
            "sort": "timestamp",
        },
    }
}

while True:
    resp = requests.post(
        f"https://api.{DD_SITE}/api/v2/llm-obs/v1/spans/events/search",
        headers=headers,
        json=payload,
    ).json()
    
    all_spans.extend(resp.get("data", []))
    
    # Check for next page cursor in response metadata
    next_cursor = resp.get("meta", {}).get("page", {}).get("after")
    if not next_cursor or not resp.get("data"):
        break
    payload["data"]["attributes"]["page"]["cursor"] = next_cursor

print(f"Fetched {len(all_spans)} total spans")
```

## What each span contains in the response

The Export API returns richly structured span objects. Key fields in each span's `attributes`:

| Field | Example | Description |
|-------|---------|-------------|
| `span_kind` | `"llm"` | Span type: llm, workflow, agent, tool, task, embedding, retrieval |
| `model_name` | `"gpt-4o-mini"` | The LLM model used |
| `model_provider` | `"openai"` | Provider name |
| `ml_app` | `"my-chatbot"` | Application name (set via `DD_LLMOBS_ML_APP`) |
| `input.messages` | `[{"role": "user", "content": "..."}]` | Structured input messages |
| `output.messages` | `[{"role": "assistant", "content": "..."}]` | Structured output messages |
| `metrics.input_tokens` | `150` | Input token count |
| `metrics.output_tokens` | `300` | Output token count |
| `metrics.estimated_total_cost` | `7500` | Estimated cost |
| `duration` | `83000` | Duration in microseconds |
| `evaluation` | `{...}` | Attached evaluation results |
| `trace_id` / `span_id` / `parent_id` | String IDs | Span relationship identifiers |
| `status` | `"ok"` or `"error"` | Span completion status |

## Why the Python SDK doesn't help here (yet)

The **`datadog-api-client`** package is auto-generated from Datadog's OpenAPI spec. As of early 2026, the LLM Observability Export API endpoints are **not included** in that spec, so there is no `LLMObservabilityApi` class. The `SpansApi` class in the SDK only wraps the APM spans endpoints (`/api/v2/spans/events`), which won't return LLM Observability data.

The **`ddtrace`** package (`pip install ddtrace`) is the instrumentation SDK — it's used to *create* LLM spans, not read them back. Its `LLMObs.export_span()` method only exports span context (trace_id + span_id) for the purpose of submitting evaluations, not for bulk data retrieval.

Your practical options today for reading LLM spans programmatically:

- **`requests` + Export API** — the recommended approach shown above
- **APM `SpansApi`** via `datadog-api-client` — only useful if you need APM-correlated spans (won't include LLM-specific input/output/token data)
- **Datadog Notebooks / Dashboards** — for visual exploration in the UI using the LLM Observability Trace Explorer query syntax (e.g., `span_kind:llm @meta.metadata.team:platform`)

## Conclusion

The source of confusion is architectural: Datadog's LLM Observability is a standalone product with its own storage, not a feature of APM. The Export API at **`/api/v2/llm-obs/v1/spans/events/search`** is the correct — and currently only — way to programmatically fetch LLM spans with full fidelity. Use raw HTTP calls with `requests` since the Python SDK hasn't caught up yet. Filter by `span_kind` to isolate LLM calls from workflow/agent/tool spans, use `tags` for custom filtering, and always specify explicit `from`/`to` timestamps since the default window is only 15 minutes. The full documentation lives at `docs.datadoghq.com/llm_observability/evaluations/export_api/` — a non-obvious location that sits under the Evaluations section rather than a top-level API reference.