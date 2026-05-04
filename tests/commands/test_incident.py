"""Tests for incident commands."""

import json
import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock
from puppy_kit.commands.incident import incident


def _make_incident(
    id,
    title,
    severity,
    status,
    created="2026-01-15T10:00:00Z",
    modified="2026-01-15T12:00:00Z",
    customer_impacted=False,
    public_id="pub-1",
    detected="2026-01-15T09:55:00Z",
    resolved=None,
):
    """Create a mock incident object."""
    inc = Mock()
    inc.id = id
    inc.type = "incidents"
    inc.public_id = public_id
    inc.attributes = Mock(
        title=title,
        severity=severity,
        state=status,
        customer_impacted=customer_impacted,
        detected=detected,
        resolved=resolved,
        created=created,
        modified=modified,
        fields={},
    )
    return inc


def _make_incident_fields_only(id, title, severity, status):
    """Create a mock incident where severity/state live only in fields payload."""
    inc = _make_incident(id, title, None, None)
    inc.attributes.fields = {
        "severity": Mock(value=severity),
        "state": Mock(value=status),
    }
    return inc


def _make_search_response(incidents, next_offset=None, offset=0, size=None):
    """Create a mock search_incidents response."""
    pagination = Mock(
        next_offset=next_offset, offset=offset, size=size if size is not None else len(incidents)
    )
    meta = Mock(pagination=pagination)
    search_results = []
    for inc in incidents:
        result = Mock()
        result.data = inc
        search_results.append(result)
    attributes = Mock(incidents=search_results, next_offset=None)
    data = Mock(attributes=attributes)
    return Mock(data=data, meta=meta)


class TestListIncidents:
    def test_list_incidents_table(self, mock_client, runner):
        """Test listing incidents in table format."""
        incidents = [
            _make_incident("inc-1", "Service outage", "SEV-1", "active"),
            _make_incident("inc-2", "Degraded performance", "SEV-3", "stable"),
        ]
        response = _make_search_response(incidents)
        mock_client.incidents.search_incidents.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "inc-1" in result.output
        assert "inc-2" in result.output
        assert "active" in result.output
        assert "stable" in result.output
        assert "Total incidents: 2" in result.output
        mock_client.incidents.search_incidents.assert_called_with(
            "", sort="-created", page_size=100, page_offset=0
        )

    def test_list_incidents_json(self, mock_client, runner):
        """Test listing incidents in JSON format."""
        incidents = [
            _make_incident("inc-1", "Service outage", "SEV-1", "active"),
            _make_incident("inc-2", "Degraded performance", "SEV-3", "stable"),
        ]
        response = _make_search_response(incidents)
        mock_client.incidents.search_incidents.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list", "--format", "json"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert len(output) == 2
        assert output[0]["id"] == "inc-1"
        assert output[0]["title"] == "Service outage"
        assert output[0]["severity"] == "SEV-1"
        assert output[0]["status"] == "active"
        assert output[0]["customer_impacted"] is False
        assert output[0]["public_id"] == "pub-1"
        assert output[0]["detected"] == "2026-01-15T09:55:00Z"
        assert output[0]["resolved"] == "unknown"
        assert output[1]["id"] == "inc-2"
        assert output[1]["title"] == "Degraded performance"
        assert output[1]["severity"] == "SEV-3"
        assert output[1]["status"] == "stable"
        mock_client.incidents.search_incidents.assert_called_with(
            "", sort="-created", page_size=100, page_offset=0
        )

    def test_list_incidents_json_uses_fields_fallback_for_state_and_severity(
        self, mock_client, runner
    ):
        """Datadog SDK may store state/severity under attributes.fields."""
        incidents = [_make_incident_fields_only("inc-1", "Service outage", "SEV-1", "stable")]
        response = _make_search_response(incidents)
        mock_client.incidents.search_incidents.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list", "--format", "json"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert output[0]["severity"] == "SEV-1"
        assert output[0]["status"] == "stable"

    def test_list_incidents_empty(self, mock_client, runner):
        """Test listing incidents when none exist."""
        response = _make_search_response([])
        mock_client.incidents.search_incidents.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "Total incidents: 0" in result.output
        mock_client.incidents.search_incidents.assert_called_with(
            "", sort="-created", page_size=100, page_offset=0
        )

    def test_list_incidents_maps_status_into_query(self, mock_client, runner):
        """Test status convenience filter is appended to the search query."""
        mock_client.incidents.search_incidents.return_value = _make_search_response([])

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(
                incident, ["list", "--query", "service:api env:prod", "--status", "active"]
            )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        mock_client.incidents.search_incidents.assert_called_with(
            "service:api env:prod state:active", sort="-created", page_size=100, page_offset=0
        )

    def test_list_incidents_since_stops_early_and_filters_page(self, mock_client, runner):
        """Test since cutoff filters the final page and stops pagination once older incidents appear."""
        recent = _make_incident(
            "inc-1", "Newest", "SEV-1", "active", created="2026-02-27T10:00:00Z"
        )
        keep = _make_incident("inc-2", "Keep", "SEV-2", "stable", created="2026-02-25T12:00:00Z")
        old = _make_incident("inc-3", "Old", "SEV-3", "resolved", created="2026-02-24T23:59:59Z")
        mock_client.incidents.search_incidents.side_effect = [
            _make_search_response([recent], next_offset=100),
            _make_search_response([keep, old], next_offset=200),
        ]

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list", "--format", "json", "--since", "2026-02-25"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert [item["id"] for item in output] == ["inc-1", "inc-2"]
        assert mock_client.incidents.search_incidents.call_count == 2

    def test_list_incidents_since_accepts_relative_hours(self, mock_client, runner):
        """Test relative since parsing for hour-based cutoffs."""
        recent = _make_incident(
            "inc-1", "Recent", "SEV-1", "active", created="2026-03-11T10:00:00Z"
        )
        old = _make_incident("inc-2", "Old", "SEV-2", "resolved", created="2026-03-10T07:59:59Z")
        mock_client.incidents.search_incidents.return_value = _make_search_response([recent, old])

        class FixedDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2026, 3, 11, 8, 0, 0, tzinfo=timezone.utc)

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.datetime", FixedDateTime):
                result = runner.invoke(
                    incident, ["list", "--format", "json", "--since", "24 hours"]
                )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert [item["id"] for item in output] == ["inc-1"]

    def test_list_incidents_rejects_invalid_since(self, mock_client, runner):
        """Test invalid since formats fail before any API call."""
        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list", "--since", "yesterday-ish"])

        assert result.exit_code != 0
        assert "Invalid --since value" in result.output
        mock_client.incidents.search_incidents.assert_not_called()

    def test_list_incidents_rejects_malformed_since_date(self, mock_client, runner):
        """Test malformed ISO date inputs fail early with a clear error."""
        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list", "--since", "2026-02-30"])

        assert result.exit_code != 0
        assert "Invalid --since value '2026-02-30'" in result.output
        mock_client.incidents.search_incidents.assert_not_called()

    def test_list_incidents_requires_desc_sort_with_since(self, mock_client, runner):
        """Test since validation rejects ascending sort because early-stop pagination depends on newest-first ordering."""
        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list", "--since", "14 days", "--sort", "created"])

        assert result.exit_code != 0
        assert "--since requires --sort=-created" in result.output
        mock_client.incidents.search_incidents.assert_not_called()


class TestGetIncident:
    def test_get_incident_table(self, mock_client, runner):
        """Test getting a single incident in table format."""
        inc = _make_incident("inc-1", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["get", "inc-1"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "inc-1" in result.output
        assert "Service outage" in result.output
        assert "SEV-1" in result.output
        assert "active" in result.output
        mock_client.incidents.get_incident.assert_called_once_with(incident_id="inc-1")

    def test_get_incident_json(self, mock_client, runner):
        """Test getting a single incident in JSON format."""
        inc = _make_incident("inc-1", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["get", "inc-1", "--format", "json"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert output["id"] == "inc-1"
        assert output["title"] == "Service outage"
        assert output["severity"] == "SEV-1"
        assert output["status"] == "active"

    def test_get_incident_json_uses_fields_fallback_for_state_and_severity(
        self, mock_client, runner
    ):
        """Incident get should surface values from attributes.fields fallback."""
        inc = _make_incident_fields_only("inc-1", "Service outage", "SEV-1", "resolved")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["get", "inc-1", "--format", "json"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert output["severity"] == "SEV-1"
        assert output["status"] == "resolved"


class TestCreateIncident:
    def test_create_incident(self, mock_client, runner):
        """Test creating an incident."""
        inc = _make_incident("inc-new", "New outage", "SEV-2", "active")
        response = Mock(data=inc)
        mock_client.incidents.create_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(
                incident,
                ["create", "--title", "New outage", "--severity", "SEV-2", "--team", "ops"],
            )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "inc-new" in result.output
        assert "created" in result.output
        assert "New outage" in result.output
        mock_client.incidents.create_incident.assert_called_once()

    def test_create_incident_json(self, mock_client, runner):
        """Test creating an incident with JSON output."""
        inc = _make_incident("inc-new", "New outage", "SEV-2", "active")
        response = Mock(data=inc)
        mock_client.incidents.create_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(
                incident,
                [
                    "create",
                    "--title",
                    "New outage",
                    "--severity",
                    "SEV-2",
                    "--team",
                    "ops",
                    "--format",
                    "json",
                ],
            )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        output = json.loads(result.output)["data"]
        assert output["id"] == "inc-new"
        assert output["severity"] == "SEV-2"

    def test_create_incident_missing_title(self, runner):
        """Test that create fails without required --title."""
        result = runner.invoke(incident, ["create", "--severity", "SEV-1"])
        assert result.exit_code != 0
        assert "Missing" in result.output or "required" in result.output.lower()

    def test_create_incident_without_severity(self, mock_client, runner):
        """Test that create succeeds without --severity (now optional)."""
        inc = _make_incident("inc-new", "Outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.create_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["create", "--title", "Outage"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        mock_client.incidents.create_incident.assert_called_once()


class TestUpdateIncident:
    def test_update_incident(self, mock_client, runner):
        """Test updating an incident."""
        inc = _make_incident("inc-1", "Updated title", "SEV-1", "stable")
        response = Mock(data=inc)
        mock_client.incidents.update_incident.return_value = response

        mock_cfg = Mock(site="datadoghq.com", api_key="test-api-key", app_key="test-app-key")
        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.load_config", return_value=mock_cfg):
                with patch("puppy_kit.commands.incident.requests.patch") as mock_patch:
                    mock_patch.return_value = Mock(raise_for_status=Mock())
                    result = runner.invoke(
                        incident,
                        ["update", "inc-1", "--title", "Updated title", "--status", "stable"],
                    )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "inc-1" in result.output
        assert "updated" in result.output
        assert "Updated title" in result.output
        mock_client.incidents.update_incident.assert_called_once()
        mock_patch.assert_called_once()

    def test_update_incident_severity_only(self, mock_client, runner):
        """Test updating only the severity of an incident."""
        inc = _make_incident("inc-1", "Service outage", "SEV-2", "active")
        response = Mock(data=inc)
        mock_client.incidents.update_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["update", "inc-1", "--severity", "SEV-2"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "updated" in result.output

    def test_update_incident_no_fields(self, runner):
        """Test that update fails when no fields are specified."""
        result = runner.invoke(incident, ["update", "inc-1"])
        assert result.exit_code != 0
        assert "No update fields" in result.output

    def test_update_incident_assignee(self, mock_client, runner):
        """Test updating an incident with assignee."""
        inc = _make_incident("inc-1", "Service outage", "SEV-1", "active")
        inc.attributes.assignee = "muhammad"
        response = Mock(data=inc)
        mock_client.incidents.update_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["update", "inc-1", "--assignee", "muhammad"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "updated" in result.output
        assert "muhammad" in result.output
        mock_client.incidents.update_incident.assert_called_once()


class TestDeleteIncident:
    def test_delete_incident_with_confirm(self, mock_client, runner):
        """Test deleting an incident with --confirm flag."""
        mock_client.incidents.delete_incident.return_value = None

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["delete", "inc-1", "--confirm"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "inc-1" in result.output
        assert "deleted" in result.output
        mock_client.incidents.delete_incident.assert_called_once_with(incident_id="inc-1")

    def test_delete_incident_interactive_yes(self, mock_client, runner):
        """Test deleting an incident with interactive confirmation (user says yes)."""
        mock_client.incidents.delete_incident.return_value = None

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["delete", "inc-1"], input="y\n")

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "deleted" in result.output
        mock_client.incidents.delete_incident.assert_called_once_with(incident_id="inc-1")

    def test_delete_incident_without_confirm(self, mock_client, runner):
        """Test that delete is aborted when user declines confirmation."""
        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["delete", "inc-1"], input="n\n")

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "Aborted" in result.output
        mock_client.incidents.delete_incident.assert_not_called()


@pytest.mark.integration
class TestTodoCommands:
    def test_todo_add(self, mock_client, runner):
        """Test adding a todo to an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        todo_response = {
            "data": {
                "id": "todo-123",
                "type": "incident_todos",
                "attributes": {"content": "Fix database connection"},
            }
        }

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.post") as mock_post:
                mock_post.return_value = MagicMock(json=lambda: todo_response)
                result = runner.invoke(
                    incident, ["todo", "add", "inc-1", "--content", "Fix database connection"]
                )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "Todo created" in result.output
        assert "todo-123" in result.output

    def test_todo_list(self, mock_client, runner):
        """Test listing todos for an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        todos_response = {
            "data": [
                {
                    "id": "todo-1",
                    "type": "incident_todos",
                    "attributes": {
                        "content": "Investigate root cause",
                        "assignees": ["@user1"],
                        "due_date": "2026-03-12",
                        "completed": None,
                    },
                },
                {
                    "id": "todo-2",
                    "type": "incident_todos",
                    "attributes": {
                        "content": "Notify stakeholders",
                        "assignees": [],
                        "due_date": None,
                        "completed": "2026-03-11T15:00:00Z",
                    },
                },
            ]
        }

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.get") as mock_get:
                mock_get.return_value = MagicMock(json=lambda: todos_response)
                result = runner.invoke(incident, ["todo", "list", "inc-1"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "todo-1" in result.output
        assert "todo-2" in result.output
        assert "Investigate root cause" in result.output

    def test_todo_complete(self, mock_client, runner):
        """Test marking a todo as complete."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.patch") as mock_patch:
                mock_patch.return_value = MagicMock()
                result = runner.invoke(incident, ["todo", "complete", "inc-1", "todo-123"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "marked complete" in result.output

    def test_todo_delete(self, mock_client, runner):
        """Test deleting a todo from an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.delete") as mock_delete:
                mock_delete.return_value = MagicMock()
                result = runner.invoke(incident, ["todo", "delete", "inc-1", "todo-123"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "deleted" in result.output


@pytest.mark.integration
class TestImpactCommands:
    def test_impact_add(self, mock_client, runner):
        """Test adding an impact to an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        impact_response = {
            "data": {
                "id": "impact-456",
                "type": "incident_impacts",
                "attributes": {"description": "Database unavailable"},
            }
        }

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.post") as mock_post:
                mock_post.return_value = MagicMock(json=lambda: impact_response)
                result = runner.invoke(
                    incident,
                    [
                        "impact",
                        "add",
                        "inc-1",
                        "--description",
                        "Database unavailable",
                        "--start",
                        "2026-03-11T17:35:52Z",
                    ],
                )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "Impact created" in result.output
        assert "impact-456" in result.output

    def test_impact_list(self, mock_client, runner):
        """Test listing impacts for an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        impacts_response = {
            "data": [
                {
                    "id": "impact-1",
                    "type": "incident_impacts",
                    "attributes": {
                        "description": "API down",
                        "start_at": "2026-03-11T17:35:00Z",
                        "end_at": "2026-03-11T17:45:00Z",
                    },
                }
            ]
        }

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.get") as mock_get:
                mock_get.return_value = MagicMock(json=lambda: impacts_response)
                result = runner.invoke(incident, ["impact", "list", "inc-1"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "impact-1" in result.output
        assert "API down" in result.output

    def test_impact_delete(self, mock_client, runner):
        """Test deleting an impact from an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.delete") as mock_delete:
                mock_delete.return_value = MagicMock()
                result = runner.invoke(incident, ["impact", "delete", "inc-1", "impact-456"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "deleted" in result.output


@pytest.mark.integration
class TestAttachmentCommands:
    def test_attachment_add(self, mock_client, runner):
        """Test adding an attachment to an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        attachment_response = {
            "data": {
                "id": "att-789",
                "type": "incident_attachments",
                "attributes": {"attachment_type": "link"},
            }
        }

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.post") as mock_post:
                mock_post.return_value = MagicMock(json=lambda: attachment_response)
                result = runner.invoke(
                    incident,
                    [
                        "attachment",
                        "add",
                        "inc-1",
                        "--url",
                        "https://github.com/org/repo/pull/123",
                        "--title",
                        "PR #123 - Fix",
                    ],
                )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "Attachment created" in result.output
        assert "att-789" in result.output

    def test_attachment_list(self, mock_client, runner):
        """Test listing attachments for an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        attachments_response = {
            "data": [
                {
                    "id": "att-1",
                    "type": "incident_attachments",
                    "attributes": {
                        "attachment_type": "link",
                        "attachment": {
                            "documentUrl": "https://github.com/org/repo/pull/123",
                            "title": "PR #123 - Fix",
                        },
                    },
                }
            ]
        }

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.get") as mock_get:
                mock_get.return_value = MagicMock(json=lambda: attachments_response)
                result = runner.invoke(incident, ["attachment", "list", "inc-1"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "att-1" in result.output
        assert "PR #123 - Fix" in result.output

    def test_attachment_delete(self, mock_client, runner):
        """Test deleting an attachment from an incident."""
        inc = _make_incident("inc-uuid", "Service outage", "SEV-1", "active")
        response = Mock(data=inc)
        mock_client.incidents.get_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            with patch("puppy_kit.commands.incident.requests.delete") as mock_delete:
                mock_delete.return_value = MagicMock()
                result = runner.invoke(incident, ["attachment", "delete", "inc-1", "att-789"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "deleted" in result.output
