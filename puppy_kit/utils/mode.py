"""Click helpers for ops-mode-aware command gating."""

import click

FULL_MODE_REQUIRED_ATTR = "_requires_full_mode"


def _get_ops_profile(ctx) -> str:
    """Walk up the Click context chain and return the active ops profile."""
    current = ctx
    while current is not None:
        if current.obj and "ops_profile" in current.obj:
            return current.obj["ops_profile"]
        current = current.parent
    return "triage"


def full_mode_only(cmd):
    """Mark a command as full-mode-only and enforce it at invocation time."""
    setattr(cmd, FULL_MODE_REQUIRED_ATTR, True)

    help_text = cmd.help or ""
    suffix = "\n\n[Requires full ops mode. Use --profile <full-profile> to enable.]"
    if suffix.strip() not in help_text:
        cmd.help = f"{help_text}{suffix}" if help_text else suffix.strip()

    original_callback = cmd.callback

    def wrapped(*args, **kwargs):
        ctx = click.get_current_context()
        if _get_ops_profile(ctx) == "triage":
            click.echo(
                (
                    f"Error: '{ctx.command.name}' requires full ops mode.\n"
                    "Current mode: triage\n\n"
                    "To enable:\n"
                    "  puppy --profile <full-profile> ...   (one-off)\n"
                    "  puppy config use-profile <full-profile>   (set default)\n"
                    "  puppy config list-profiles               (view profiles)"
                ),
                err=True,
            )
            ctx.exit(1)

        if original_callback is None:
            return None
        return original_callback(*args, **kwargs)

    cmd.callback = wrapped
    return cmd


class ModeAwareGroup(click.Group):
    """Click group that hides full-mode-only commands in triage mode."""

    def list_commands(self, ctx):
        command_names = super().list_commands(ctx)
        if _get_ops_profile(ctx) != "triage":
            return command_names

        visible = []
        for name in command_names:
            command = click.Group.get_command(self, ctx, name)
            if not getattr(command, FULL_MODE_REQUIRED_ATTR, False):
                visible.append(name)
        return visible

    def get_command(self, ctx, cmd_name):
        return super().get_command(ctx, cmd_name)
