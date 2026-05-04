# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

puppy-kit is a Datadog CLI + optional MCP server for AI-driven incident management. 22 command groups, 100+ subcommands, Rich terminal output, retry logic, structured JSON output, stdin piping, and investigation workflows. Requires Python 3.10+.

## Commands

```bash
# Setup
uv sync --all-extras                              # --all-extras required for dev tools

# Run tests
uv run pytest tests/ -v
uv run pytest tests/commands/test_apm.py -v        # single module
uv run pytest tests/commands/test_apm.py::test_name # single test
uv run pytest tests/ --cov=puppy_kit --cov-report=html
uv run pytest tests/ -m "not integration"           # skip integration tests

# Code quality
uv run ruff format puppy_kit/ tests/                # format (line-length: 100)
uv run ruff check puppy_kit/ tests/                 # lint (line-length: 100)
uv run ty                                           # type check

# Run CLI
export DD_API_KEY=... DD_APP_KEY=...
uv run puppy monitor list --state Alert
uv run puppy apm services
uv run puppy logs search "status:error" --service my-api
uv run puppy investigate latency my-service --threshold 500
uv run puppy monitor list --state Alert --watch 10
```

## Architecture

**Entry point**: `puppy_kit.cli:main` — a Click group (`AliasGroup`) that registers command subgroups. Two entry points: `puppy` and `puppy-kit`.

**Command groups** (`puppy_kit/commands/`): Each file defines a Click group with subcommands. Commands call `get_datadog_client()` to get an API client, then use Rich for output formatting. All commands support `--format json|table`.
- **Defensive attribute access**: Use `getattr(obj, "attr", default)` for optional attributes. API responses vary by source.

```
puppy monitor      {list, get, create, update, delete, mute, unmute, validate, mute-all, unmute-all}
puppy metric       {query, search, metadata}
puppy event        {list, get, post}
puppy host         {list, get, totals}
puppy apm          {services, traces, analytics}
puppy logs         {search, tail, query, trace}
puppy dbm          {hosts, queries, explain, samples}
puppy investigate  {latency, errors, throughput, compare}
puppy dashboard    {list, get, create, update, delete, export, clone}
puppy slo          {list, get, create, update, delete, history, export}
puppy downtime     {list, get, create, update, delete, cancel-by-scope}
puppy tag          {list, add, replace, detach}
puppy service-check {post}
puppy synthetics   {list, get, results, trigger}
puppy incident     {list, get, create, update, delete}
puppy notebook     {list, get, create, delete}
puppy user         {list, get, invite, disable}
puppy usage        {summary, hosts, logs, top-avg-metrics}
puppy rum          {events, analytics}
puppy ci           {pipelines, tests, pipeline-details}
puppy config       {init, set-profile, use-profile, list-profiles, get}
puppy apply        -f <file> [--dry-run] [--recursive]
puppy diff         -f <file>
puppy completion   {bash, zsh, fish}
```

**Aliases**: `mon`=monitor, `dash`=dashboard, `dt`=downtime, `sc`=service-check, `inv`=investigate

**Key modules**:
- `puppy_kit/client.py` — `DatadogClient` wraps `datadog_api_client` SDK. V1 APIs: monitors, metrics, events, hosts, tags, service_checks, downtimes, slos, dashboards, usage, synthetics, notebooks. V2 APIs: logs, spans, service_definitions, incidents, users, rum, ci_pipelines, ci_tests. Use `get_datadog_client()` to instantiate.
- `puppy_kit/config.py` — `DatadogConfig` (Pydantic BaseSettings) loads from env vars (`DD_API_KEY`, `DD_APP_KEY`, `DD_SITE`) or `~/.puppy-kit/config.json` profiles. Supports region shortcuts (us, eu, us3, us5, ap1, gov). Precedence: CLI `--profile` flag > `PUPPY_KIT_PROFILE` env var > active profile > defaults.
- `puppy_kit/mcp/server.py` — FastMCP server exposing Datadog operations as tools for AI agents. Optional dependency (`pip install puppy-kit[mcp]`).
- `puppy_kit/utils/error.py` — `@handle_api_error` decorator with retry logic (exponential backoff on 429/5xx, immediate exit on 401/403). Emits structured JSON errors when `--format json`.
- `puppy_kit/utils/exit_codes.py` — Semantic exit codes: 0=success, 1=general, 2=auth, 3=not found, 4=validation, 5=rate limited, 6=server error.

## Testing Patterns

Tests use `unittest.mock` with Click's `CliRunner`. Key fixtures from `tests/conftest.py`:
- `mock_client` — Mock with all API attributes
- `runner` — `CliRunner()` instance
- Standard test pattern: patch `get_datadog_client` to return `mock_client`, invoke command via `runner`, assert on output and exit code.

## Development Workflow

- **Worktrees**: Always create a Git worktree for every new feature, fix, or change.
- **Pull requests**: Every change lands via PR — no direct commits to `main`.
- **Commits**: Follow conventional commit format.
- **CI**: Tests run on Python 3.10-3.13 + `claude-review` AI code review.

## Versioning

Dynamic versioning via **hatch-vcs** — version is derived from git tags (`v*.*.*`). No hardcoded version anywhere. The `puppy_kit/_version.py` file is auto-generated at build time.

## Releasing

1. Tag: `git tag -a vX.Y.Z -m "vX.Y.Z"` and `git push origin vX.Y.Z`
2. CI publish job auto-triggers on `refs/tags/v*` via PyPI trusted publishing
