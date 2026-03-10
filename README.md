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

### Environment Variables

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
export DD_SITE="us"  # optional, defaults to datadoghq.com
```

### Interactive Setup

```bash
puppy config init
```

This creates `~/.puppy-kit/config.json` with your credentials.

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

### Region Shortcuts

| Shortcut | Site |
|----------|------|
| `us` | `datadoghq.com` |
| `eu` | `datadoghq.eu` |
| `us3` | `us3.datadoghq.com` |
| `us5` | `us5.datadoghq.com` |
| `ap1` | `ap1.datadoghq.com` |
| `gov` | `ddog-gov.com` |

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
