# Ops Modes: Triage, Active, and Full

## Overview

puppy-kit supports three **ops profiles** that control which Datadog operations are available:

- **Triage mode** (default): Read-only and incident-management focused. Allows operators to investigate incidents, triage issues, and manage incident lifecycle (create, update, delete, attach, link). Suitable for on-call engineers who should not modify production monitoring, dashboards, or SLOs.

- **Active mode**: Identical to triage mode (read-only, same permissions). A named preset that scopes help output and documentation to only the command groups relevant to your active Datadog products (based on your billing data). Useful for teams with specific product stacks who want focused guidance on available tools.

- **Full mode**: Superset of triage. Includes all write operations across the entire Datadog platform: create/modify monitors, dashboards, SLOs, downtimes, synthetics, service definitions, and more. Suitable for platform engineers, SREs, and automation workflows that need complete control.

The restriction is enforced at the **SDK level** (`datadog_api_client`), not at the CLI command level. All 22 command groups are always registered; attempting to use a disabled operation in triage mode will raise an SDK error.

## How to Configure

### Interactive Setup

Create a new profile interactively:

```bash
puppy config init
```

You will be prompted for API key, app key, site, ops profile (triage, active, or full), and profile name.

### Command Line

Create or update a profile with `set-profile`:

```bash
# Create a triage profile (default)
puppy config set-profile myprofile \
  --api-key "..." \
  --app-key "..." \
  --site us \
  --ops-profile triage

# Create an active profile (triage with focused help)
puppy config set-profile active-agent \
  --api-key "..." \
  --app-key "..." \
  --site us \
  --ops-profile active

# Create a full-access profile
puppy config set-profile admin \
  --api-key "..." \
  --app-key "..." \
  --site us \
  --ops-profile full
```

### Profile Selection

Use a specific profile:

```bash
puppy incident list --profile myprofile
puppy monitor create ... --profile admin
```

Set the active profile globally:

```bash
puppy config use-profile myprofile
```

View all profiles:

```bash
puppy config list-profiles
```

### Environment Variables

Override profile selection via environment:

```bash
# Use a named profile
export PUPPY_KIT_PROFILE=myprofile
puppy incident list

# Or override auth directly (uses default "triage" ops profile)
export DD_API_KEY="..." DD_APP_KEY="..." DD_SITE=us
puppy incident list
```

## Precedence

Profile and ops mode selection follows this priority:

1. CLI `--profile` flag (highest priority)
2. `PUPPY_KIT_PROFILE` environment variable
3. `active_profile` in `~/.puppy-kit/config.json`
4. Hardcoded defaults (datadoghq.com, triage mode)

## Active Mode Operations

Active mode provides **identical read-only permissions to triage mode**. The difference is semantic: it signals that the profile is scoped to your organization's active Datadog product stack. This is useful for on-call teams, AI agents, and automation that should only interact with the products your team actively uses.

Active mode is appropriate for the following products:
- APM & Serverless
- Incident Management
- Infrastructure Monitoring (Hosts)
- Database Monitoring
- CI Visibility
- Log Management
- RUM & Session Replay
- Metrics

All commands in triage mode are available in active mode; it does not restrict any operations compared to triage.

## Triage Mode Operations

Triage mode enables incident management, case linking, and read-only access to security and observability data. These operations are always available:

### Incident Management (Full CRUD)

- Incidents: create, list, search, get, update, delete
- Incident attachments: create, list, get, update, delete
- Incident integrations: create, list, get, update, delete
- Incident notification rules: create, list, get, update, delete
- Incident notification templates: create, list, get, update, delete
- Incident postmortem templates: create, list, get, update, delete
- Incident postmortem attachments: create
- Incident todos: create, list, get, update, delete
- Incident types: create, list, get, update, delete
- Incident services: create, list, get, update, delete
- Incident teams: create, list, get, update, delete
- Incident team members: add, list, remove
- Global incident handles: create, list, get, update, delete
- Global incident settings: get, update

### Case Management (Linking & Integration)

- Case notebooks: create
- Case Jira issues: create, link, unlink
- Case ServiceNow tickets: create
- Case project operations: move
- Incident linking: link incidents

### Security & Vulnerability (Read-Only)

- Findings: list, get
- Vulnerabilities: list
- Vulnerable assets: list
- Scanned assets metadata: list
- Security monitoring signals: list, search, get by job ID
- Security monitoring rules: get rule version history, get secrets rules
- Threat hunting jobs: list, get

### SLOs (Read-Only)

- SLO reports: create job, get report, get job status
- SLO status: get

### Code Observability (Read-Only)

- Code coverage: get branch summary, get commit summary
- Flaky tests: search, update

### LLM Observability (Read-Only)

- LLM datasets: list, list records
- LLM experiments: list
- LLM projects: list

### Integration & Third-Party (Read-Only)

- Connections: list
- Account mappings: get, query accounts
- User queries: list, get, query
- Jira accounts: list, list issue templates, get template
- ServiceNow instances: list, list templates, get template, list assignment groups, list business services, list users
- Tenancy configs: get
- HAMR org connection: get

### Monitoring & Deployment (Read-Only)

- Monitor templates: list, get, validate
- Restriction queries: list, get
- Role restriction queries: list, get
- Datasets: list, get
- Custom rules: get, list revisions
- Fleet agents: list, get info, list versions
- Fleet deployments: list, get
- Fleet schedules: list, get
- Change requests: get
- Deployment gates: get, get rules
- Deployment rules: get
- AWS cloud auth persona mappings: list, get
- Rulesets: list
- Content packs: get states
- APIs: list, get OpenAPI spec
- Role templates: list

## Full Mode Operations

Full mode enables all triage operations **plus** write access to the entire Datadog platform. The additional operations not in triage mode include:

- **Monitor management**: create, update, delete monitors (all variants)
- **Dashboard management**: create, update, delete dashboards
- **Downtime management**: create, update, delete, cancel downtimes
- **SLO management**: create, update, delete SLOs
- **Synthetics management**: create, update, delete synthetic tests
- **Service definitions**: create, update, delete service definitions
- **Custom rules & rulesets**: create, update, delete custom rules and rulesets
- **Alert/notification settings**: configure rules, templates, routing
- **Organization settings**: manage users, teams, roles, and permissions
- **Advanced deployments**: create, update deployment gates and rules
- **Data pipeline configuration**: configure data deletion requests, retention policies

To see the exact set of additional operations, inspect `FULL_ONLY_UNSTABLE_OPS` in `puppy_kit/client.py`.

## Configuration File Example

`~/.puppy-kit/config.json`:

```json
{
  "active_profile": "default",
  "profiles": {
    "default": {
      "api_key": "da...",
      "app_key": "xyz...",
      "site": "datadoghq.com",
      "ops_profile": "triage"
    },
    "active-agent": {
      "api_key": "da...",
      "app_key": "abc...",
      "site": "datadoghq.com",
      "ops_profile": "active"
    },
    "admin": {
      "api_key": "da...",
      "app_key": "def...",
      "site": "datadoghq.com",
      "ops_profile": "full"
    },
    "eu-staging": {
      "api_key": "da...",
      "app_key": "ghi...",
      "site": "datadoghq.eu",
      "ops_profile": "triage"
    }
  }
}
```

## Troubleshooting

**"Operation X is not enabled"**

You are using a triage profile. Switch to full mode or use a full-access profile:

```bash
puppy config use-profile admin
# or
puppy <command> --profile admin
```

**"Profile not found"**

Check available profiles:

```bash
puppy config list-profiles
```

Ensure the profile name matches exactly and that `~/.puppy-kit/config.json` exists.

**"Configuration error"**

Verify environment variables are set correctly:

```bash
echo $DD_API_KEY $DD_APP_KEY $DD_SITE
```

Or check the active profile:

```bash
puppy config get active_profile
```

## Best Practices

1. **Use triage by default**: Create triage profiles for on-call rotations and incident management.
2. **Separate admin profiles**: Use full-access profiles only when explicitly needed for platform changes.
3. **Environment-specific profiles**: Create separate profiles for staging and production with appropriate ops modes.
4. **Use --profile flag in scripts**: When invoking puppy-kit from automation, specify `--profile` explicitly to avoid ambiguity.
5. **Rotate API keys regularly**: Treat `~/.puppy-kit/config.json` as sensitive; set permissions to 0600 (puppy-kit does this automatically).
