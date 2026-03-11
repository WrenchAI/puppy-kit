"""Tests for CLI mode gating helpers."""

from unittest.mock import Mock

import click

from puppy_kit.utils.mode import ModeAwareGroup, _get_ops_profile, full_mode_only


@click.group(cls=ModeAwareGroup)
@click.pass_context
def gated_cli(ctx):
    """Test CLI."""
    ctx.ensure_object(dict)


@gated_cli.command(name="read")
def read_cmd():
    """Read command."""
    click.echo("read")


@full_mode_only
@gated_cli.command(name="write")
def write_cmd():
    """Write command."""
    click.echo("write")


def test_full_mode_only_hidden_in_triage(runner):
    result = runner.invoke(gated_cli, ["--help"], obj={"ops_profile": "triage"})

    assert result.exit_code == 0
    assert "read" in result.output
    assert "write" not in result.output


def test_full_mode_only_visible_in_full(runner):
    result = runner.invoke(gated_cli, ["--help"], obj={"ops_profile": "full"})

    assert result.exit_code == 0
    assert "read" in result.output
    assert "write" in result.output


def test_full_mode_only_blocked_in_triage(runner):
    result = runner.invoke(gated_cli, ["write"], obj={"ops_profile": "triage"})

    assert result.exit_code == 1
    assert "requires full ops mode" in result.output
    assert "Current mode: triage" in result.output


def test_full_mode_only_allowed_in_full(runner):
    result = runner.invoke(gated_cli, ["write"], obj={"ops_profile": "full"})

    assert result.exit_code == 0
    assert result.output.strip() == "write"


def test_get_ops_profile_defaults_to_triage():
    ctx = Mock()
    ctx.obj = None
    ctx.parent = None

    assert _get_ops_profile(ctx) == "triage"
