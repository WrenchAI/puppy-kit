"""Main CLI entry point for puppy-kit."""

import sys

import click
from click.exceptions import Abort, BadParameter, MissingParameter, UsageError
from rich.console import Console
from puppy_kit.env import TRACE_ENABLED
from puppy_kit import trace_logger


def _parse_cmd_from_argv(argv):
    """Parse command and arguments from sys.argv.

    Returns (cmd, arguments) tuple.
    Example: ['puppy', 'incident', 'list', '--sort', '-created']
             -> ('incident list', '--sort -created')
    """
    if len(argv) <= 1:
        return ("-", "")

    parts = argv[1:]  # Skip executable name

    # Separate non-flag tokens (command parts) from flag tokens
    cmd_tokens = [a for a in parts if not a.startswith("-")]

    # Command is first 1-2 command tokens (group and subcommand)
    if len(cmd_tokens) >= 2:
        cmd = " ".join(cmd_tokens[:2])
    elif len(cmd_tokens) == 1:
        cmd = cmd_tokens[0]
    else:
        cmd = "-"

    # Arguments are everything after the first 2 command tokens
    cmd_token_count = 2 if len(cmd_tokens) >= 2 else len(cmd_tokens)
    remaining = parts[cmd_token_count:] if cmd_token_count < len(parts) else []
    arguments = " ".join(remaining) if remaining else "-"

    return (cmd, arguments)


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
    """puppy-kit: Datadog CLI for AI-driven incident triage.

    Compact, LLM-optimised read-only CLI for querying Datadog.

    Commands: monitor, metric, event, host, apm, logs, dbm, service-check,
    tag, downtime, dashboard, rum, incident, user, usage, ci, cost, llm.

    Configuration:
        DD_API_KEY - Datadog API key (required)
        DD_APP_KEY - Datadog Application key (required)
        DD_SITE - Datadog site (default: datadoghq.com)

    Examples:
        puppy config test
        puppy monitor list --limit 5
        puppy apm services --from 24h
        puppy logs search "status:error" --from 1h --limit 10
    """
    ctx.ensure_object(dict)
    ctx.obj["profile"] = profile
    # Store trace context for end-of-invocation logging
    if TRACE_ENABLED:
        cmd, arguments = _parse_cmd_from_argv(sys.argv)
        ctx.obj["_trace"] = {
            "cmd": cmd,
            "args": arguments,
            "full": " ".join(sys.argv),
        }


# Import and register all command groups
# ruff: noqa: E402
from puppy_kit.commands.monitor import monitor
from puppy_kit.commands.metric import metric
from puppy_kit.commands.event import event
from puppy_kit.commands.host import host
from puppy_kit.commands.apm import apm
from puppy_kit.commands.logs import logs
from puppy_kit.commands.service_check import service_check
from puppy_kit.commands.tag import tag
from puppy_kit.commands.downtime import downtime
from puppy_kit.commands.dashboard import dashboard
from puppy_kit.commands.rum import rum
from puppy_kit.commands.config import config
from puppy_kit.commands.incident import incident
from puppy_kit.commands.user import user
from puppy_kit.commands.usage import usage
from puppy_kit.commands.ci import ci
from puppy_kit.commands.cost import cost
from puppy_kit.commands.llm import llm

main.add_command(monitor)
main.add_command(metric)
main.add_command(event)
main.add_command(host)
main.add_command(apm)
main.add_command(logs)
main.add_command(service_check)
main.add_command(tag)
main.add_command(downtime)
main.add_command(dashboard)
main.add_command(rum)
main.add_command(config)
main.add_command(incident)
main.add_command(user)
main.add_command(usage)
main.add_command(ci)
main.add_command(cost)
main.add_command(llm)


def run() -> None:
    """Entry point wrapper — invokes main() and writes CMD trace with exit status."""
    _status = "ok"
    _error = "-"
    _trace: dict | None = None
    cmd, args = _parse_cmd_from_argv(sys.argv)
    _trace = {
        "cmd": cmd,
        "args": args,
        "full": " ".join(sys.argv),
    }

    try:
        main()
    except SystemExit as e:
        code = int(e.code) if e.code is not None else 0
        if code == 0:
            _status = "ok"
        elif code == 2:
            _status = "input"
        else:
            _status = "error"
            _error = f"exit {code}"
        raise
    except (UsageError, BadParameter, MissingParameter) as e:
        _status = "input"
        _error = e.format_message()
        raise
    except Abort:
        _status = "input"
        _error = "aborted"
        raise
    except Exception as e:
        _status = "error"
        _error = str(e)
        raise
    finally:
        if TRACE_ENABLED and _trace:
            trace_logger.info(
                f"CMD | {_trace['cmd']} | {_trace['args']} | {_status} | - | {_trace['full']} | {_error}"
            )


if __name__ == "__main__":
    run()
