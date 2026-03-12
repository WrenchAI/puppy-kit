"""Tests for LLM Observability commands."""

import json
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock


def _create_mock_project(project_id, name, created_at=None):
    """Create a mock LLM project."""
    if created_at is None:
        created_at = datetime.now()

    attrs = Mock()
    attrs.name = name
    attrs.description = f"Project {name}"
    attrs.created_at = created_at
    attrs.updated_at = created_at

    project = Mock()
    project.id = project_id
    project.type = "llm_obs_project"
    project.attributes = attrs
    return project


def test_projects_table(mock_client, runner):
    """Test projects command displays table with correct headers and data."""
    from puppy_kit.commands.llm import llm

    projects = [
        _create_mock_project("proj-001", "Production LLM"),
        _create_mock_project("proj-002", "Testing LLM"),
    ]
    mock_response = Mock(data=projects)
    mock_client.llm_observability.list_llm_obs_projects.return_value = mock_response

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        result = runner.invoke(llm, ["projects"])

        assert result.exit_code == 0
        assert "LLM Observability Projects" in result.output
        assert "Production LLM" in result.output
        assert "Testing LLM" in result.output
        assert "Total projects: 2" in result.output


def test_projects_json(mock_client, runner):
    """Test projects command outputs valid JSON with expected fields."""
    from puppy_kit.commands.llm import llm

    projects = [
        _create_mock_project("proj-json-001", "Test Project"),
    ]
    mock_response = Mock(data=projects)
    mock_client.llm_observability.list_llm_obs_projects.return_value = mock_response

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        result = runner.invoke(llm, ["projects", "--format", "json"])

        assert result.exit_code == 0
        output = json.loads(result.output)["data"]
        assert len(output) == 1
        assert output[0]["id"] == "proj-json-001"
        assert output[0]["name"] == "Test Project"


def test_projects_empty(mock_client, runner):
    """Test projects command with no results shows total 0."""
    from puppy_kit.commands.llm import llm

    mock_response = Mock(data=[])
    mock_client.llm_observability.list_llm_obs_projects.return_value = mock_response

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        result = runner.invoke(llm, ["projects"])

        assert result.exit_code == 0
        assert "Total projects: 0" in result.output


def _create_mock_span(
    span_id,
    model,
    span_kind,
    status="ok",
    ml_app=None,
    input_tokens=10,
    output_tokens=20,
    duration_us=500000,
    span_name=None,
    trace_id=None,
):
    """Create a mock LLM Obs span."""
    # Generate a unique trace_id based on span_id if not provided
    if trace_id is None:
        trace_id = f"trace-{span_id.split('-')[-1]}"

    return {
        "id": span_id,
        "attributes": {
            "span_id": span_id,
            "trace_id": trace_id,
            "parent_id": "0000000000000000",
            "start_ns": 1000000000,
            "span_kind": span_kind,
            "name": span_name or f"span-{span_kind}",
            "model_name": model,
            "model_provider": "openai",
            "ml_app": ml_app or "default",
            "status": status,
            "duration": duration_us,
            "input": f"Sample input for {model}",
            "output": f"Sample output from {model}",
            "metrics": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_total_cost": 0.001,
            },
        },
    }


def test_traces_table(mock_client, runner):
    """Test traces command displays table with correct headers and span data."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-001", "gpt-4o", "llm"),
            _create_mock_span("span-002", "gpt-4o-mini", "agent"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(llm, ["traces", "--from", "1h", "--mode", "all"])

            assert result.exit_code == 0
            assert "LLM Observability Spans" in result.output
            assert "Total traces: 2" in result.output


def test_traces_json(mock_client, runner):
    """Test traces command outputs valid JSON with span data."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "us5.datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-json-001", "gpt-4o", "llm"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(llm, ["traces", "--mode", "all", "--format", "json"])

            assert result.exit_code == 0
            output = json.loads(result.output)["data"]
            assert len(output) == 1
            # Verify the flattened structure (not nested attributes)
            assert output[0]["kind"] == "llm"
            assert output[0]["input_tokens"] == 10
            assert output[0]["output_tokens"] == 20
            assert output[0]["model"] == "gpt-4o"
            assert "span_id" in output[0]
            assert "name" in output[0]


def test_traces_empty(mock_client, runner):
    """Test traces command with no results shows total 0."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {"data": []}

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(llm, ["traces"])

            assert result.exit_code == 0
            assert "Total traces: 0" in result.output


def test_traces_span_kind_filter(mock_client, runner):
    """Test traces command filters by name (client-side)."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-001", "gpt-4o", "agent", span_name="FindEntityIdTool"),
            _create_mock_span("span-002", "gpt-4o", "agent", span_name="OtherTool"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(
                llm, ["traces", "--name", "FindEntityIdTool", "--mode", "all", "--format", "json"]
            )

            assert result.exit_code == 0
            output = json.loads(result.output)["data"]
            # Should return only the span matching the name
            assert len(output) == 1
            # Access flattened structure, not nested attributes
            assert output[0]["name"] == "FindEntityIdTool"


def test_traces_ml_app_filter(mock_client, runner):
    """Test traces command filters by ml_app."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-001", "gpt-4o", "llm", ml_app="ai-axis"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(llm, ["traces", "--ml-app", "ai-axis"])

            assert result.exit_code == 0
            call_args = mock_post.call_args
            payload = call_args.kwargs["json"]
            assert payload["data"]["attributes"]["filter"]["tags"]["ml_app"] == "ai-axis"


def test_traces_model_filter_client_side(mock_client, runner):
    """Test traces command filters by model name on the client side."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-001", "gpt-4o", "llm"),
            _create_mock_span("span-002", "gpt-4o-mini", "llm"),
            _create_mock_span("span-003", "claude-3-opus", "llm"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(
                llm, ["traces", "--model", "gpt-4o", "--mode", "all", "--format", "json"]
            )

            assert result.exit_code == 0
            output = json.loads(result.output)["data"]
            assert len(output) == 2
            # Verify flattened structure with "model" key (not "attributes")
            assert all("gpt-4o" in item["model"] for item in output)


def test_traces_mode_error_filter(mock_client, runner):
    """Test traces command filters by mode=error on the client side."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-001", "gpt-4o", "llm", status="ok"),
            _create_mock_span("span-002", "gpt-4o", "llm", status="error"),
            _create_mock_span("span-003", "gpt-4o", "llm", status="ok"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(llm, ["traces", "--mode", "error", "--format", "json"])

            assert result.exit_code == 0
            output = json.loads(result.output)["data"]
            assert len(output) == 1
            assert output[0]["status"] == "error"


def test_traces_name_and_mode_combined(mock_client, runner):
    """Test traces command with combined --name and --mode filters."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    mock_response_data = {
        "data": [
            _create_mock_span("span-001", None, "tool", status="ok", span_name="FindEntityIdTool"),
            _create_mock_span(
                "span-002", None, "tool", status="error", span_name="FindEntityIdTool"
            ),
            _create_mock_span("span-003", None, "tool", status="error", span_name="OtherTool"),
        ]
    }

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200, json=MagicMock(return_value=mock_response_data)
            )

            result = runner.invoke(
                llm, ["traces", "--name", "FindEntityIdTool", "--mode", "error", "--format", "json"]
            )

            assert result.exit_code == 0
            output = json.loads(result.output)["data"]
            # Should return only FindEntityIdTool error span
            assert len(output) == 1
            # Access flattened structure, not nested attributes
            assert output[0]["name"] == "FindEntityIdTool"
            assert output[0]["status"] == "error"


def test_traces_api_permission_error(mock_client, runner):
    """Test traces command handles 403 permission error gracefully."""
    from puppy_kit.commands.llm import llm

    mock_client.config.api_key = "test-api-key"
    mock_client.config.app_key = "test-app-key"
    mock_client.config.site = "datadoghq.com"

    with patch("puppy_kit.commands.llm.get_datadog_client", return_value=mock_client):
        with patch("puppy_kit.commands.llm.requests.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=403)

            result = runner.invoke(llm, ["traces"])

            assert result.exit_code != 0
            assert "403" in result.output
            assert "permissions" in result.output.lower()
