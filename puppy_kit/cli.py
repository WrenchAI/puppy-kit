"""Main CLI entry point for puppy-kit."""

import click
from rich.console import Console

console = Console()


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


class AliasGroup(click.Group):
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
