# Operations Guide

## Command Set

puppy-kit provides 18 command groups covering incident management, monitoring, logging, APM, and more:

- **Incident Management**: `incident` — Full CRUD for incidents, attachments, integrations, and notifications
- **Monitoring**: `monitor`, `downtime`, `metric`, `event`, `service-check`, `tag`
- **Logging & Tracing**: `logs`, `apm`, `dbm`
- **Dashboards & Visibility**: `dashboard`, `host`, `usage`, `rum`, `ci`
- **Advanced Analytics**: `cost`, `llm`, `user`
- **Configuration**: `config`

All commands support structured output via `--format json` and full output with `--verbose` where applicable.

## Configuration

### Quick Setup

```bash
puppy config init
```

This prompts for `DD_API_KEY`, `DD_APP_KEY`, and optional `DD_SITE`, then stores credentials in `~/.puppy-kit/config.json`.

### Environment Variables

```bash
export DD_API_KEY="..."
export DD_APP_KEY="..."
export DD_SITE="us"  # optional, defaults to datadoghq.com
puppy incident list
```

### Verify Setup

```bash
puppy config test
```

This validates your credentials against Datadog.

## Usage Examples

```bash
# List incidents
puppy incident list

# Search logs
puppy logs search "status:error" --service my-api --verbose

# Query metrics
puppy metric query "avg:system.cpu{env:prod}" --from 1h

# Export as JSON
puppy monitor list --format json

# Validate configuration
puppy config test
```

## Security

- Store `~/.puppy-kit/config.json` securely; puppy-kit sets permissions to 0600 automatically
- Rotate API keys regularly
- Use environment variables for temporary or scripted access
- Never commit credentials to version control
