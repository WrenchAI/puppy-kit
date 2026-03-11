# Ops Modes

## Overview

`puppy` supports two ops modes through the profile field `ops_profile`:

- `triage`: safe default for incident response, investigation, and read-heavy workflows
- `full`: unlocks infrastructure-changing operations and administrative commands

The CLI loads `ops_profile` from the selected profile and defaults to `triage` if config loading fails.

## CLI-layer gating

CLI-layer gating keeps full-mode-only commands out of normal triage help while preserving direct help access.

- Command groups use `ModeAwareGroup` to hide full-only subcommands from `--help` when `ops_profile` is `triage`
- Full-only commands still resolve through `get_command`, so `puppy <group> <command> --help` remains available
- Commands marked with `@full_mode_only` print a mode error and exit with status `1` when invoked in triage mode
- The root CLI exposes `--help-triage` to print a triage reference guide and exit

The current CLI-gated commands are:

- `monitor`: `create`, `update`, `delete`, `mute`, `unmute`, `mute-all`, `unmute-all`
- `dashboard`: `create`, `update`, `delete`, `clone`
- `slo`: `create`, `update`, `delete`
- `downtime`: `create`, `update`, `delete`, `cancel-by-scope`
- `synthetics`: `trigger`
- `event`: `post`
- `tag`: `add`, `replace`, `detach`
- `notebook`: `create`, `delete`
- `user`: `invite`, `disable`
- `service-check`: `post`
- `apply`

Use a full profile for one-off access:

```bash
puppy --profile <full-profile> monitor create ...
```

Or switch the default profile:

```bash
puppy config use-profile <full-profile>
puppy config list-profiles
```
