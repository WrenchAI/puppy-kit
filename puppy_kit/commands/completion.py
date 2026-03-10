"""Shell completion commands."""

import click


@click.group(invoke_without_command=True)
@click.pass_context
def completion(ctx):
    """Generate shell completion scripts.

    Output shell-specific completion scripts for bash, zsh, or fish.

    Usage:
        eval "$(puppy completion bash)"
        eval "$(puppy completion zsh)"
        puppy completion fish | source
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@completion.command()
def bash():
    """Output bash completion script."""
    click.echo('eval "$(_PUPPY_COMPLETE=bash_source puppy_kit)"')


@completion.command()
def zsh():
    """Output zsh completion script."""
    click.echo('eval "$(_PUPPY_COMPLETE=zsh_source puppy_kit)"')


@completion.command()
def fish():
    """Output fish completion script."""
    click.echo("_PUPPY_COMPLETE=fish_source puppy_kit | source")
