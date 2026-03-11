"""Main CLI entry point for puppy-kit."""

import click
from rich.console import Console
from puppy_kit.utils.mode import ModeAwareGroup, full_mode_only

console = Console()
__all__ = ("AliasGroup", "ModeAwareGroup", "TRIAGE_HELP_TEXT", "full_mode_only", "main")


def _get_version() -> str:
    """Get package version from hatch-vcs generated file, with fallback."""
    try:
        from puppy_kit._version import __version__

        return __version__
    except ImportError:
        return "0.0.0-dev"


# Command aliases: short name -> full command name
ALIASES = {
    "mon": "monitor",
    "dash": "dashboard",
    "dt": "downtime",
    "sc": "service-check",
    "inv": "investigate",
}

TRIAGE_HELP_TEXT = """puppy triage mode reference

Overview
  Triage mode is the default ops profile for puppy.
  It is intended for incident response, investigation, and read-heavy workflows.
  Full mode unlocks infrastructure-changing commands that are hidden in triage help.

How mode is selected
  1. `puppy --profile <name> ...`
  2. `PUPPY_KIT_PROFILE=<name>`
  3. Active profile from `~/.puppy-kit/config.json`
  4. Fallback mode: `triage`

How gating works
  Commands marked as full-only are hidden from `--help` in triage mode.
  The command still resolves so `puppy <group> <cmd> --help` continues to work.
  Running a gated command in triage prints an error and exits with code 1.

Enable full mode
  One-off:
    puppy --profile <full-profile> <command>
  Set default profile:
    puppy config use-profile <full-profile>
  Inspect profiles:
    puppy config list-profiles

Recommended profile setup
  Create at least one triage profile for agents and automation.
  Create a separate full profile for administrative or infrastructure changes.
  Keep the full profile scoped to humans or controlled break-glass paths.

Typical triage-safe workflows
  puppy monitor list --state Alert
  puppy incident list --sort -created
  puppy logs search "status:error" --service my-api
  puppy apm traces my-service --from 1h
  puppy investigate latency my-service --threshold 500

Commands gated at the CLI layer
  monitor: create, update, delete, mute, unmute, mute-all, unmute-all
  dashboard: create, update, delete, clone
  slo: create, update, delete
  downtime: create, update, delete, cancel-by-scope
  synthetics: trigger
  event: post
  tag: add, replace, detach
  notebook: create, delete
  user: invite, disable
  service-check: post
  apply

What stays available in triage
  Read and investigation commands remain visible in normal help.
  Incident CRUD remains available because incident response is a core workflow.
  Direct `--help` on a gated command remains available for discovery.

Examples
  Show triage-visible commands:
    puppy --help
  Show the triage reference:
    puppy --help-triage
  Show help for a gated command:
    puppy monitor create --help
  Run a gated command with a full profile:
    puppy --profile prod-admin monitor create --type "metric alert" --query "..."

Expected error for gated commands in triage
  Error: '<cmd_name>' requires full ops mode.
  Current mode: triage

  To enable:
    puppy --profile <full-profile> ...   (one-off)
    puppy config use-profile <full-profile>   (set default)
    puppy config list-profiles               (view profiles)

Troubleshooting
  If a command is missing from help, check the profile's `ops_profile`.
  Use `puppy config list-profiles` to inspect available profile names.
  If config loading fails, CLI help falls back to triage behavior.
  Environment variables can still override the selected profile credentials.

Related files
  Docs: docs/ops-modes.md
  Config field: `ops_profile`
  Values: `triage`, `full`

Summary
  Use triage for safe investigation defaults.
  Use full only when you intend to make Datadog changes.
  Keep separate profiles for those two operating modes.
"""


def _show_triage_help(ctx, param, value):
    """Print the triage-mode reference guide and exit."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(TRIAGE_HELP_TEXT)
    ctx.exit()


class AliasGroup(ModeAwareGroup):
    """Click Group subclass that supports command aliases."""

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        # Check aliases
        if cmd_name in ALIASES:
            return click.Group.get_command(self, ctx, ALIASES[cmd_name])
        return None

    def resolve_command(self, ctx, args):
        # Always resolve alias to the full command name
        cmd_name = args[0] if args else None
        if cmd_name in ALIASES:
            args = [ALIASES[cmd_name]] + args[1:]
        return super().resolve_command(ctx, args)


@click.group(cls=AliasGroup)
@click.version_option(version=_get_version())
@click.option(
    "--profile",
    default=None,
    envvar="PUPPY_KIT_PROFILE",
    help="Configuration profile to use (from ~/.puppy-kit/config.json).",
)
@click.option(
    "--help-triage",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_show_triage_help,
    help="Print triage mode reference guide and exit.",
)
@click.pass_context
def main(ctx, profile):
    """puppy-kit: Datadog CLI + MCP server for AI-driven incident management.

    Query monitors, metrics, events, hosts, APM traces, logs, and more
    from your terminal with rich output and smart defaults.

    Configuration:
        DD_API_KEY - Datadog API key (required)
        DD_APP_KEY - Datadog Application key (required)
        DD_SITE - Datadog site (default: datadoghq.com)

    Examples:
        puppy monitor list --state Alert
        puppy apm traces my-service --from 1h
        puppy logs search "status:error" --service my-api
    """
    ctx.ensure_object(dict)
    ctx.obj["profile"] = profile
    try:
        from puppy_kit.config import load_config

        _config = load_config(profile=profile)
        ctx.obj["ops_profile"] = _config.ops_profile
    except Exception:
        ctx.obj["ops_profile"] = "triage"


# Import and register all command groups
# ruff: noqa: E402
from puppy_kit.commands.monitor import monitor
from puppy_kit.commands.metric import metric
from puppy_kit.commands.event import event
from puppy_kit.commands.host import host
from puppy_kit.commands.apm import apm
from puppy_kit.commands.logs import logs
from puppy_kit.commands.dbm import dbm
from puppy_kit.commands.investigate import investigate
from puppy_kit.commands.service_check import service_check
from puppy_kit.commands.tag import tag
from puppy_kit.commands.downtime import downtime
from puppy_kit.commands.slo import slo
from puppy_kit.commands.dashboard import dashboard
from puppy_kit.commands.synthetics import synthetics
from puppy_kit.commands.rum import rum
from puppy_kit.commands.notebook import notebook
from puppy_kit.commands.completion import completion
from puppy_kit.commands.apply import apply_cmd, diff_cmd
from puppy_kit.commands.config import config
from puppy_kit.commands.incident import incident
from puppy_kit.commands.user import user
from puppy_kit.commands.usage import usage
from puppy_kit.commands.ci import ci

main.add_command(monitor)
main.add_command(metric)
main.add_command(event)
main.add_command(host)
main.add_command(apm)
main.add_command(logs)
main.add_command(dbm)
main.add_command(investigate)
main.add_command(service_check)
main.add_command(tag)
main.add_command(downtime)
main.add_command(slo)
main.add_command(dashboard)
main.add_command(synthetics)
main.add_command(rum)
main.add_command(notebook)
main.add_command(completion)
main.add_command(apply_cmd)
main.add_command(diff_cmd)
main.add_command(config)
main.add_command(incident)
main.add_command(user)
main.add_command(usage)
main.add_command(ci)


if __name__ == "__main__":
    main()
