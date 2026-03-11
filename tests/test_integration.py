"""Live integration tests — require real Datadog credentials.

Skipped automatically if DD_API_KEY or DD_APP_KEY are not set.
Tests warn (not fail) on empty responses.

Run:
    DD_API_KEY=... DD_APP_KEY=... DD_SITE=... uv run pytest tests/test_integration.py -v
"""

import os
import pytest
import warnings
from click.testing import CliRunner
from puppy_kit.cli import main


@pytest.fixture(scope="session", autouse=True)
def skip_if_no_credentials():
    """Skip all tests in this module if DD_API_KEY or DD_APP_KEY are not set."""
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")

    if not api_key or not app_key:
        pytest.skip(
            "Integration tests skipped: DD_API_KEY or DD_APP_KEY not set",
            allow_module_level=True,
        )


@pytest.fixture
def runner():
    """Click CLI test runner."""
    return CliRunner()


class TestIntegration:
    """Live integration tests against real Datadog API."""

    def test_config_test(self, runner):
        """Test puppy config test command."""
        result = runner.invoke(main, ["config", "test"])
        assert result.exit_code in (0, 2), f"Unexpected exit code: {result.output}"
        # Should either succeed or fail with auth error
        if result.exit_code == 0:
            assert "Auth OK" in result.output or "✓" in result.output

    def test_monitor_list(self, runner):
        """Test puppy monitor list --limit 5."""
        result = runner.invoke(main, ["monitor", "list", "--limit", "5"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        # Warn if empty (not a failure)
        if "No monitors" in result.output or result.output.strip() == "":
            warnings.warn("Monitor list returned empty results")

    def test_incident_list(self, runner):
        """Test puppy incident list --limit 5."""
        result = runner.invoke(main, ["incident", "list", "--limit", "5"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No incidents" in result.output or result.output.strip() == "":
            warnings.warn("Incident list returned empty results")

    def test_dashboard_list(self, runner):
        """Test puppy dashboard list --limit 5."""
        result = runner.invoke(main, ["dashboard", "list", "--limit", "5"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No dashboards" in result.output or result.output.strip() == "":
            warnings.warn("Dashboard list returned empty results")

    def test_logs_search(self, runner):
        """Test puppy logs search "status:error" --limit 5 --from 1h."""
        result = runner.invoke(
            main, ["logs", "search", "status:error", "--limit", "5", "--from", "1h"]
        )
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No logs" in result.output or result.output.strip() == "":
            warnings.warn("Logs search returned empty results")

    def test_apm_services(self, runner):
        """Test puppy apm services."""
        result = runner.invoke(main, ["apm", "services"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No services" in result.output or result.output.strip() == "":
            warnings.warn("APM services returned empty results")

    def test_metric_query(self, runner):
        """Test puppy metric query "avg:system.cpu.user{*}" --from 1h."""
        result = runner.invoke(main, ["metric", "query", "avg:system.cpu.user{*}", "--from", "1h"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No data" in result.output or result.output.strip() == "":
            warnings.warn("Metric query returned empty results")

    def test_host_list(self, runner):
        """Test puppy host list --limit 5."""
        result = runner.invoke(main, ["host", "list", "--limit", "5"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No hosts" in result.output or result.output.strip() == "":
            warnings.warn("Host list returned empty results")

    def test_event_list(self, runner):
        """Test puppy event list --limit 5 --from 24h."""
        result = runner.invoke(main, ["event", "list", "--limit", "5", "--from", "24h"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No events" in result.output or result.output.strip() == "":
            warnings.warn("Event list returned empty results")

    def test_rum_events(self, runner):
        """Test puppy rum events --limit 5 --from 1h."""
        result = runner.invoke(main, ["rum", "events", "--limit", "5", "--from", "1h"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No events" in result.output or result.output.strip() == "":
            warnings.warn("RUM events returned empty results")

    def test_cost_summary(self, runner):
        """Test puppy cost summary."""
        result = runner.invoke(main, ["cost", "summary"])
        assert result.exit_code == 0, f"Command failed: {result.output}"

    def test_llm_traces(self, runner):
        """Test puppy llm traces --limit 5 --from 24h."""
        result = runner.invoke(main, ["llm", "traces", "--limit", "5", "--from", "24h"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No traces" in result.output or result.output.strip() == "":
            warnings.warn("LLM traces returned empty results")

    def test_user_list(self, runner):
        """Test puppy user list --limit 5."""
        result = runner.invoke(main, ["user", "list", "--limit", "5"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No users" in result.output or result.output.strip() == "":
            warnings.warn("User list returned empty results")

    def test_dbm_hosts(self, runner):
        """Test puppy dbm hosts."""
        result = runner.invoke(main, ["dbm", "hosts"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No hosts" in result.output or result.output.strip() == "":
            warnings.warn("DBM hosts returned empty results")

    def test_ci_pipelines(self, runner):
        """Test puppy ci pipelines --limit 5."""
        result = runner.invoke(main, ["ci", "pipelines", "--limit", "5"])
        assert result.exit_code == 0, f"Command failed: {result.output}"
        if "No pipelines" in result.output or result.output.strip() == "":
            warnings.warn("CI pipelines returned empty results")

    def test_usage_summary(self, runner):
        """Test puppy usage summary."""
        result = runner.invoke(main, ["usage", "summary"])
        assert result.exit_code == 0, f"Command failed: {result.output}"

    def test_tag_list(self, runner):
        """Test puppy tag list --host localhost."""
        result = runner.invoke(main, ["tag", "list", "localhost"])
        # Tag list might fail if host doesn't exist, which is OK
        assert result.exit_code in (0, 3), f"Unexpected exit code: {result.output}"
