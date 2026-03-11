"""Tests for incident commands."""

import json
from datetime import datetime, timezone
from unittest.mock import Mock, patch
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
        status=status,
        customer_impacted=customer_impacted,
        detected=detected,
        resolved=resolved,
        created=created,
        modified=modified,
        fields={},
    )
    return inc


def _make_search_response(incidents, next_offset=None, offset=0, size=None):
    """Create a mock search_incidents response."""
    pagination = Mock(
        next_offset=next_offset, offset=offset, size=size if size is not None else len(incidents)
    )
    meta = Mock(pagination=pagination)
    return Mock(included=incidents, meta=meta)


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
            "", sort="-created", page_size=10, page_offset=0
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
        output = json.loads(result.output)
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
            "", sort="-created", page_size=10, page_offset=0
        )

    def test_list_incidents_empty(self, mock_client, runner):
        """Test listing incidents when none exist."""
        response = _make_search_response([])
        mock_client.incidents.search_incidents.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(incident, ["list"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "Total incidents: 0" in result.output
        mock_client.incidents.search_incidents.assert_called_with(
            "", sort="-created", page_size=10, page_offset=0
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
            "service:api env:prod state:active", sort="-created", page_size=10, page_offset=0
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
        output = json.loads(result.output)
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
        output = json.loads(result.output)
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
        output = json.loads(result.output)
        assert output["id"] == "inc-1"
        assert output["title"] == "Service outage"
        assert output["severity"] == "SEV-1"
        assert output["status"] == "active"


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
        output = json.loads(result.output)
        assert output["id"] == "inc-new"
        assert output["severity"] == "SEV-2"

    def test_create_incident_missing_title(self, runner):
        """Test that create fails without required --title."""
        result = runner.invoke(incident, ["create", "--severity", "SEV-1"])
        assert result.exit_code != 0
        assert "Missing" in result.output or "required" in result.output.lower()

    def test_create_incident_missing_severity(self, runner):
        """Test that create fails without required --severity."""
        result = runner.invoke(incident, ["create", "--title", "Outage", "--team", "ops"])
        assert result.exit_code != 0
        assert "Missing" in result.output or "required" in result.output.lower()


class TestUpdateIncident:
    def test_update_incident(self, mock_client, runner):
        """Test updating an incident."""
        inc = _make_incident("inc-1", "Updated title", "SEV-1", "stable")
        response = Mock(data=inc)
        mock_client.incidents.update_incident.return_value = response

        with patch("puppy_kit.commands.incident.get_datadog_client", return_value=mock_client):
            result = runner.invoke(
                incident, ["update", "inc-1", "--title", "Updated title", "--status", "stable"]
            )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "inc-1" in result.output
        assert "updated" in result.output
        assert "Updated title" in result.output
        mock_client.incidents.update_incident.assert_called_once()

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
