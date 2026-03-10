# puppy-kit

**Datadog CLI + MCP server for AI-driven incident management.**

A modern CLI for the Datadog API with 22 command groups, 100+ subcommands, Rich terminal output, retry logic, and an optional MCP server that lets AI agents (Claude Code, Codex) detect, triage, and resolve incidents autonomously.

Forked from [ddogctl](https://github.com/srgfrancisco/ddogctl) by Sergio Francisco (MIT License).

## Features

- 22 command groups covering monitors, incidents, logs, APM, dashboards, SLOs, and more
- Rich terminal output with tables, colors, and progress indicators
- Investigation workflows that correlate across monitors, traces, logs, and hosts
- Optional MCP server exposing Datadog operations as tools for AI agents
- Retry logic with exponential backoff on rate limits and server errors
- Multi-profile configuration with region shortcuts
- Per-profile ops mode: `triage` (safe default) or `full` (all operations unlocked)
- Watch mode, stdin piping, JSON export, and shell completions

## Installation

```bash
pip install puppy-kit
```

With [uv](https://docs.astral.sh/uv/):

```bash
uv pip install puppy-kit
```

With MCP server support:

```bash
pip install puppy-kit[mcp]
```

## Configuration

### Getting Your Credentials

Before using puppy-kit, you need two API keys from Datadog:

- **`DD_API_KEY`** — Your organization's API key. Found in Datadog at **Organization Settings > API Keys**. This key is scoped to your organization and used for sending and reading data (metrics, logs, events, etc.).

- **`DD_APP_KEY`** — Your personal application key. Found in Datadog at **Organization Settings > Application Keys**. This key is scoped to your user account and is required for management operations such as creating/updating monitors, dashboards, logs queries, and other admin tasks. Granting all scopes is recommended for personal use.

**Important:** Both keys are required for most `puppy` commands. Without `DD_APP_KEY`, you will receive a 403 Unauthorized error on most read and write operations.

To locate these in the Datadog UI:
1. Log in to [Datadog](https://app.datadoghq.com)
2. Click your user icon (bottom left) → **Organization Settings**
3. Select **API Keys** or **Application Keys** from the left sidebar
4. Copy the key or generate a new one

### Environment Variables

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
export DD_SITE="us"  # optional, defaults to datadoghq.com
```

**Note:** `DD_SITE` is a shortcut (see [Region Shortcuts](#region-shortcuts) below). For example, use `us5` to point to `us5.datadoghq.com`.

### Interactive Setup

```bash
puppy config init
```

This command prompts you interactively for your `DD_API_KEY`, `DD_APP_KEY`, and optional `DD_SITE`, then creates `~/.puppy-kit/config.json` with your credentials.

### Multi-Profile

```bash
puppy config set-profile staging --api-key xxx --app-key yyy --site eu
puppy config use-profile staging
puppy config list-profiles
```

Select a profile per-command with `--profile`:

```bash
puppy --profile production monitor list
```

Or via environment variable:

```bash
export PUPPY_KIT_PROFILE=production
```

### Ops Profile

Each profile has an `ops_profile` setting that controls which Datadog API operations are available:

| Profile | What's enabled |
|---------|---------------|
| `triage` (default) | Incident management (full CRUD), case linking, read-only triage ops (findings, scorecard, SLO reports, flaky tests, LLM observability, security signals, etc.) |
| `full` | Everything in `triage` plus infrastructure setup ops: fleet management, deployment gates, API catalog, Jira/ServiceNow integration config, restriction policies, data deletion, SCA rules, and more |

Set it during `puppy config init` (prompted automatically), or explicitly:

```bash
# Set on an existing profile
puppy config set-profile --ops-profile full

# Or in ~/.puppy-kit/config.json
{
  "profiles": {
    "Wrench": {
      "api_key": "...",
      "app_key": "...",
      "site": "us5.datadoghq.com",
      "ops_profile": "triage"
    }
  }
}
```

Use `triage` for AI agents and automated tooling. Use `full` only when you need to manage Datadog infrastructure directly.

### Region Shortcuts

| Shortcut | Site |
|----------|------|
| `us` | `datadoghq.com` |
| `eu` | `datadoghq.eu` |
| `us3` | `us3.datadoghq.com` |
| `us5` | `us5.datadoghq.com` |
| `ap1` | `ap1.datadoghq.com` |
| `gov` | `ddog-gov.com` |

### Verify Connectivity

After setting up your credentials, test the connection:

```bash
puppy config get          # confirm keys are loaded
puppy monitor list        # test authenticated read
```

If you see a 403 Unauthorized error, ensure both `DD_API_KEY` and `DD_APP_KEY` are set and have the correct values.

## Quick Start

```bash
# Monitors
puppy monitor list --state Alert
puppy monitor get 12345
puppy monitor mute 12345

# Incidents
puppy incident list
puppy incident create --title "API latency spike" --severity SEV-2
puppy incident update abc123 --status resolved

# Logs
puppy logs search "status:error" --service my-api --from 30m
puppy logs tail "env:prod"

# APM
puppy apm services
puppy apm traces my-service --from 1h

# Metrics
puppy metric query "avg:system.cpu.user{env:prod}" --from 1h

# Dashboards
puppy dashboard list
puppy dashboard get abc-def-123

# Investigation Workflows
puppy investigate latency my-service --threshold 500
puppy investigate errors my-service --from 1h
puppy investigate compare my-service --from 1h --baseline 24h

# Watch mode (auto-refresh)
puppy monitor list --state Alert --watch 10
```

## Commands

| Command | Subcommands |
|---------|-------------|
| `monitor` / `mon` | list, get, create, update, delete, mute, unmute, validate, mute-all, unmute-all |
| `incident` | list, get, create, update, delete |
| `logs` | search, tail, query, trace |
| `apm` | services, traces, analytics |
| `metric` | query, search, metadata |
| `event` | list, get, post |
| `host` | list, get, totals |
| `dashboard` / `dash` | list, get, create, update, delete, export, clone |
| `slo` | list, get, create, update, delete, history, export |
| `downtime` / `dt` | list, get, create, update, delete, cancel-by-scope |
| `investigate` / `inv` | latency, errors, throughput, compare |
| `dbm` | hosts, queries, explain, samples |
| `synthetics` | list, get, results, trigger |
| `tag` | list, add, replace, detach |
| `service-check` / `sc` | post |
| `notebook` | list, get, create, delete |
| `user` | list, get, invite, disable |
| `usage` | summary, hosts, logs, top-avg-metrics |
| `rum` | events, analytics |
| `ci` | pipelines, tests, pipeline-details |
| `config` | init, set-profile, use-profile, list-profiles, get |
| `apply` | Apply Datadog resources from JSON files |
| `diff` | Compare local JSON against live Datadog state |
| `completion` | bash, zsh, fish |

All commands support `--format json` for machine-readable output.

## MCP Server

puppy-kit includes an optional [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes Datadog operations as tools for AI agents.

### Setup

Install with MCP support:

```bash
pip install puppy-kit[mcp]
```

### Available Tools

| Tool | Description |
|------|-------------|
| `dd_monitors_list` | List monitors with optional filtering |
| `dd_monitors_get` | Get monitor details |
| `dd_monitors_create` | Create a monitor |
| `dd_monitors_delete` | Delete a monitor |
| `dd_monitors_mute` | Mute a monitor |
| `dd_monitors_unmute` | Unmute a monitor |
| `dd_incidents_list` | List incidents |
| `dd_incidents_get` | Get incident details |
| `dd_incidents_create` | Create an incident |
| `dd_incidents_update` | Update an incident |
| `dd_incidents_delete` | Delete an incident |
| `dd_downtimes_list` | List downtimes |
| `dd_downtimes_create` | Create a downtime |
| `dd_downtimes_cancel` | Cancel a downtime |
| `dd_logs_search` | Search logs |
| `dd_metrics_query` | Query metrics |
| `dd_events_create` | Create an event |
| `dd_events_search` | Search events |
| `dd_dashboards_list` | List dashboards |
| `dd_dashboards_get` | Get dashboard details |
| `dd_hosts_list` | List hosts |
| `dd_slos_list` | List SLOs |
| `dd_slos_get` | Get SLO details |

### Claude Code Integration

Add to your Claude Code MCP config:

```json
{
  "mcpServers": {
    "puppy-kit": {
      "command": "python",
      "args": ["-m", "puppy_kit.mcp.server"],
      "env": {
        "DD_API_KEY": "your-api-key",
        "DD_APP_KEY": "your-app-key"
      }
    }
  }
}
```

## Development

```bash
# Clone and install
git clone https://github.com/WrenchAI/puppy-kit.git
cd puppy-kit
uv sync --all-extras

# Run tests
uv run pytest tests/ -v

# Lint and format
uv run ruff check puppy_kit/ tests/
uv run ruff format puppy_kit/ tests/

# Run CLI in development
uv run puppy --help
```

## Attribution

- Original project: [ddogctl](https://github.com/srgfrancisco/ddogctl) by Sergio Francisco
- License: MIT (preserved)
- Fork maintained by: [WrenchAI](https://github.com/WrenchAI)

## License

[MIT](./LICENSE)
