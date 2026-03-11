# puppy-kit: Transformation Plan

## Origin

Forked from [srgfrancisco/ddogctl](https://github.com/srgfrancisco/ddogctl) (MIT License) into [WrenchAI/puppy-kit](https://github.com/WrenchAI/puppy-kit).

ddogctl is a modern Datadog CLI — 22 command groups, 100+ subcommands, Rich output, retry logic, investigation workflows. The fork preserves full attribution and git history.

## Goal

Transform ddogctl into **puppy-kit**: a Datadog CLI + optional MCP server that AI agents (Claude Code, Codex) can use to detect, triage, document, and resolve incidents autonomously.

## Two Codebases

| | **puppy-kit** (this repo) | **dd-cli** (prototype) |
|---|---|---|
| **Path** | `C:\Users\willem\Documents\WrenchProjects\puppy-kit` | `C:\Users\willem\Documents\PythonProjects\dd_cli` |
| **Origin** | Fork of srgfrancisco/ddogctl | Built from scratch |
| **Package dir** | `ddogctl/` (to be renamed `puppy_kit/`) | `src/dd_cli/` |
| **Commands** | 22 groups, 100+ subcommands | 7 groups (incidents, monitors, downtimes, logs, metrics, events, dashboards) |
| **MCP server** | None | Yes — FastMCP server exposing all services as tools |
| **Models** | Empty `models/` dir | Pydantic models for all inputs/outputs |
| **Services** | Commands call SDK directly | Service layer between CLI and SDK |
| **Config** | Multi-profile, region shortcuts | Simple env + JSON fallback |
| **Error handling** | `@handle_api_error` decorator with retry + semantic exit codes | Exception hierarchy |
| **Utilities** | watch, stdin, file input, export, confirm, tags, time, spans | Basic output formatting |
| **Tests** | 90+ tests | 35 tests |
| **Linting** | black + ruff | ruff |

**Decision**: puppy-kit (the ddogctl fork) is the foundation. We port the MCP server and Pydantic models from dd-cli into it.

## What ddogctl Already Has (Keep All)

### Commands
- `monitor` — list, get, create, update, delete, mute, unmute, mute-all, unmute-all, validate
- `metric` — query, search, metadata
- `event` — list, get, post
- `host` — list, get, totals
- `apm` — services, traces, analytics
- `logs` — search, tail, query, trace
- `dbm` — hosts, queries, explain, samples
- `investigate` — latency, errors, throughput, compare
- `dashboard` — list, get, create, update, delete, export, clone
- `slo` — list, get, create, update, delete, history, export
- `downtime` — list, get, create, update, delete, cancel-by-scope
- `tag` — list, add, replace, detach
- `service-check` — post
- `synthetics` — list, get, results, trigger
- `incident` — list, get, create, update, delete
- `notebook` — list, get, create, delete
- `user` — list, get, invite, disable
- `usage` — summary, hosts, logs, top-avg-metrics
- `rum` — events, analytics
- `ci` — pipelines, tests, pipeline-details
- `config` — init, set-profile, use-profile, list-profiles, get
- `apply/diff` — declarative resource management from JSON files
- `completion` — bash, zsh, fish

### Architecture (Keep)
- Unified `DatadogClient` wrapping all V1 + V2 APIs + custom DBM client
- Multi-profile config with region shortcuts (us, eu, us3, us5, ap1, gov)
- `@handle_api_error` decorator with exponential backoff retry on 429/5xx
- Semantic exit codes (0-6)
- Watch mode, stdin piping, file input, JSON export, confirmation prompts
- Command aliases (`mon`, `dash`, `dt`, `sc`, `inv`)

## What We're Adding

### 1. Package Rename (`ddogctl` → `puppy_kit`)
- Rename directory: `ddogctl/` → `puppy_kit/`
- Find-replace all imports: `ddogctl` → `puppy_kit`
- Config path: `~/.ddogctl/` → `~/.puppy-kit/`
- CLI entry point: `ddogctl` → `puppy`
- Env var: `DDOGCTL_PROFILE` → `PUPPY_KIT_PROFILE`

### 2. MCP Server (from dd-cli)
Port `dd_cli/mcp/server.py` → `puppy_kit/mcp/server.py`, adapted to call ddogctl's existing client/commands.

FastMCP server exposing Datadog operations as native tools for Claude Code. Each tool has typed parameters and docstrings the LLM reads. Optional dependency — CLI works without it.

### 3. Deployment (WrenchCL Pattern)
- **hatch-vcs**: Dynamic versioning from git tags (`v*.*.*`), no hardcoded version
- **GitHub Actions**: Tag push → auto-build → PyPI Trusted Publishing (OIDC)
- **CI**: Tests + lint on PR/push to main

### 4. Tooling Alignment
- Drop black — use **ruff format** + **ruff check** only
- Type checking via **ty** (not mypy)
- Python 3.10+ (keep broad compat from original)

### 5. CLAUDE.md
Project-specific development guidelines for this repo.

## Transformation Steps

### Step 1: Rename package
```
git mv ddogctl puppy_kit
```
Find-replace `ddogctl` → `puppy_kit` in all `.py` files, tests, and config.

### Step 2: Update pyproject.toml
- Name: `puppy-kit`
- Version: `dynamic = ["version"]` via hatch-vcs
- Build requires: `hatchling>=1.24.2`, `hatch-vcs>=0.4.0`
- Entry point: `puppy = "puppy_kit.cli:main"`
- Add `mcp[cli]>=1.0` as optional dependency
- Drop black, add ruff as sole formatter/linter
- Authors: Willem van der Schans (maintainer), original author credited in LICENSE/git history
- URLs: point to WrenchAI/puppy-kit

### Step 3: Add GitHub Actions
- `.github/workflows/publish-uv.yml` — tag-triggered PyPI publish (WrenchCL pattern)
- `.github/workflows/run-tests.yml` — PR/push test + lint

### Step 4: Add MCP server
- `puppy_kit/mcp/__init__.py`
- `puppy_kit/mcp/server.py` — FastMCP tools wrapping existing `get_datadog_client()` + command logic

### Step 5: Verify
```bash
uv sync
uv run pytest tests/ -v
uv run ruff check puppy_kit/ tests/
uv run ruff format --check puppy_kit/ tests/
uv run puppy --help
```

### Step 6: CLAUDE.md + README update

## Config Format (preserved from ddogctl)

`~/.puppy-kit/config.json`:
```json
{
  "active_profile": "default",
  "profiles": {
    "default": { "api_key": "...", "app_key": "...", "site": "us" },
    "production": { "api_key": "...", "app_key": "...", "site": "eu" }
  }
}
```

Env vars override: `DD_API_KEY`, `DD_APP_KEY`, `DD_SITE`.
Profile selection: `--profile` flag > `PUPPY_KIT_PROFILE` env var > `active_profile` from config.

## Attribution

- Original project: [ddogctl](https://github.com/srgfrancisco/ddogctl) by Sergio Francisco
- License: MIT (preserved in LICENSE file)
- Fork maintained by: WrenchAI
