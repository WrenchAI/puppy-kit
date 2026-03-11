"""Unified Datadog API client wrapper."""

import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api import (
    monitors_api,
    metrics_api,
    events_api,
    hosts_api,
    tags_api,
    service_checks_api,
    downtimes_api,
    service_level_objectives_api,
    dashboards_api,
    usage_metering_api,
    synthetics_api,
    notebooks_api,
)
from datadog_api_client.v2.api import (
    logs_api,
    spans_api,
    service_definition_api,
    incidents_api,
    users_api,
    rum_api,
    ci_visibility_pipelines_api,
    ci_visibility_tests_api,
    llm_observability_api,
)
from puppy_kit import trace_logger
from puppy_kit.env import TRACE_ENABLED, DEBUG_ENABLED
from puppy_kit.config import DatadogConfig


class _Namespace:
    """Simple namespace for attribute access on API response data."""

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class _Response:
    """Minimal response wrapper with a .data attribute."""

    def __init__(self, data):
        self.data = data


def _unstable_op_name(operation_key: str) -> str:
    """Normalize SDK unstable operation key to bare operation name."""
    return operation_key.split(".", 1)[1] if "." in operation_key else operation_key


"""Unstable operations enabled for the triage profile (incidents + read-oriented triage)."""
TRIAGE_UNSTABLE_OPS: set[str] = {
    # Incident management (full CRUD — core purpose of the tool)
    "create_global_incident_handle",
    "delete_global_incident_handle",
    "list_global_incident_handles",
    "update_global_incident_handle",
    "get_global_incident_settings",
    "update_global_incident_settings",
    "create_incident",
    "delete_incident",
    "get_incident",
    "update_incident",
    "list_incidents",
    "search_incidents",
    "import_incident",
    "create_incident_attachment",
    "delete_incident_attachment",
    "list_incident_attachments",
    "update_incident_attachment",
    "create_incident_integration",
    "delete_incident_integration",
    "get_incident_integration",
    "list_incident_integrations",
    "update_incident_integration",
    "create_incident_notification_rule",
    "delete_incident_notification_rule",
    "get_incident_notification_rule",
    "list_incident_notification_rules",
    "update_incident_notification_rule",
    "create_incident_notification_template",
    "delete_incident_notification_template",
    "get_incident_notification_template",
    "list_incident_notification_templates",
    "update_incident_notification_template",
    "create_incident_postmortem_attachment",
    "create_incident_postmortem_template",
    "delete_incident_postmortem_template",
    "get_incident_postmortem_template",
    "list_incident_postmortem_templates",
    "update_incident_postmortem_template",
    "create_incident_todo",
    "delete_incident_todo",
    "get_incident_todo",
    "list_incident_todos",
    "update_incident_todo",
    "create_incident_type",
    "delete_incident_type",
    "get_incident_type",
    "list_incident_types",
    "update_incident_type",
    "create_incident_service",
    "delete_incident_service",
    "get_incident_service",
    "list_incident_services",
    "update_incident_service",
    "add_member_team",
    "create_incident_team",
    "delete_incident_team",
    "get_incident_team",
    "list_incident_teams",
    "list_member_teams",
    "remove_member_team",
    "update_incident_team",
    # Case management (triage linking)
    "create_case_jira_issue",
    "create_case_notebook",
    "create_case_service_now_ticket",
    "link_incident",
    "link_jira_issue_to_case",
    "move_case_to_project",
    "unlink_jira_issue",
    # Read-only triage ops
    "get_finding",
    "list_findings",
    "list_vulnerabilities",
    "list_vulnerable_assets",
    "list_scanned_assets_metadata",
    "get_rule_version_history",
    "get_secrets_rules",
    "get_security_monitoring_histsignal",
    "get_security_monitoring_histsignals_by_job_id",
    "list_security_monitoring_histsignals",
    "search_security_monitoring_histsignals",
    "list_threat_hunting_jobs",
    "get_threat_hunting_job",
    "list_scorecard_outcomes",
    "list_scorecard_rules",
    "list_scorecard_outcomes",
    "list_entity_risk_scores",
    "create_slo_report_job",
    "get_slo_report",
    "get_slo_report_job_status",
    "get_slo_status",
    "get_spa_recommendations",
    "get_spa_recommendations_with_shard",
    "get_code_coverage_branch_summary",
    "get_code_coverage_commit_summary",
    "search_flaky_tests",
    "list_llm_obs_datasets",
    "list_llm_obs_dataset_records",
    "list_llm_obs_experiments",
    "list_llm_obs_projects",
    "get_data_deletion_requests",
    "list_apis",
    "get_open_api",
    "list_role_templates",
    "list_restriction_queries",
    "get_restriction_query",
    "list_restriction_query_roles",
    "list_user_restriction_queries",
    "get_role_restriction_query",
    "list_monitor_user_templates",
    "get_monitor_user_template",
    "validate_existing_monitor_user_template",
    "validate_monitor_user_template",
    "list_connections",
    "get_mapping",
    "get_account_facet_info",
    "get_user_facet_info",
    "query_accounts",
    "query_event_filtered_users",
    "query_users",
    "list_jira_accounts",
    "list_jira_issue_templates",
    "get_jira_issue_template",
    "list_service_now_instances",
    "list_service_now_templates",
    "get_service_now_template",
    "list_service_now_assignment_groups",
    "list_service_now_business_services",
    "list_service_now_users",
    "get_tenancy_configs",
    "get_hamr_org_connection",
    "get_all_datasets",
    "get_dataset",
    "get_custom_rule",
    "get_custom_rule_revision",
    "get_custom_ruleset",
    "list_custom_rule_revisions",
    "get_fleet_agent_info",
    "list_fleet_agents",
    "list_fleet_agent_versions",
    "list_fleet_deployments",
    "get_fleet_deployment",
    "list_fleet_schedules",
    "get_fleet_schedule",
    "get_change_request",
    "get_deployment_gate",
    "get_deployment_gate_rules",
    "get_deployment_rule",
    "get_aws_cloud_auth_persona_mapping",
    "list_aws_cloud_auth_persona_mappings",
    "list_multiple_rulesets",
    "get_content_packs_states",
    "list_llm_obs_dataset_records",
    "update_flaky_tests",
}

_SDK_UNSTABLE_OP_KEYS: frozenset[str] = frozenset(
    _unstable_op_name(k) for k in Configuration().unstable_operations.values
)

"""Unstable operations excluded from triage and only enabled by the full profile."""
FULL_ONLY_UNSTABLE_OPS: frozenset[str] = frozenset(
    _unstable_op_name(operation_key)
    for operation_key in _SDK_UNSTABLE_OP_KEYS
    if _unstable_op_name(operation_key) not in TRIAGE_UNSTABLE_OPS
)


class DBMClient:
    """Lightweight wrapper for DBM API endpoints using direct HTTP calls."""

    def __init__(self, api_client):
        self._api_client = api_client

    def _call(self, method, path, **query_params):
        """Make a direct REST call through the SDK's ApiClient."""
        params = {k: v for k, v in query_params.items() if v is not None}
        response = self._api_client.call_api(
            path, method, query_params=params, header_params={"Accept": "application/json"}
        )
        import json

        body = json.loads(response.response.data) if response.response.data else {}
        data_raw = body.get("data", [])
        if isinstance(data_raw, list):
            return _Response(
                [_Namespace(item) if isinstance(item, dict) else item for item in data_raw]
            )
        elif isinstance(data_raw, dict):
            return _Response(_Namespace(data_raw))
        return _Response(data_raw)

    def list_hosts(self, **kwargs):
        return self._call("GET", "/api/v2/dbm/hosts", **kwargs)

    def list_queries(self, **kwargs):
        return self._call("GET", "/api/v2/dbm/activity", **kwargs)

    def get_query_plan(self, query_id, **kwargs):
        return self._call("GET", f"/api/v2/dbm/query/{query_id}/plan", **kwargs)

    def list_query_samples(self, query_id, **kwargs):
        return self._call("GET", f"/api/v2/dbm/query/{query_id}/samples", **kwargs)


class DatadogClient:
    """Unified Datadog API client."""

    def __init__(self, config: DatadogConfig):
        self.config = config
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = config.api_key
        configuration.api_key["appKeyAuth"] = config.app_key
        configuration.server_variables["site"] = config.site
        enabled_ops = (
            TRIAGE_UNSTABLE_OPS
            if config.ops_profile == "triage"
            else TRIAGE_UNSTABLE_OPS | FULL_ONLY_UNSTABLE_OPS
        )
        for op in enabled_ops:
            if op in configuration.unstable_operations:
                configuration.unstable_operations[op] = True

        proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
        if proxy:
            configuration.proxy = proxy

        self.api_client = ApiClient(configuration)
        if (TRACE_ENABLED or DEBUG_ENABLED) and not hasattr(self.api_client, "_original_call_api"):
            self.api_client._original_call_api = self.api_client.call_api

            def traced_call_api(resource_path, method, *args, **kwargs):
                status = "-"
                try:
                    result = self.api_client._original_call_api(
                        resource_path, method, *args, **kwargs
                    )
                    # Try to extract status from result
                    if hasattr(result, "status"):
                        status = str(result.status)
                    elif isinstance(result, tuple) and len(result) >= 2:
                        status = str(result[1])

                    if DEBUG_ENABLED:
                        import sys
                        import json

                        print(f"\n[DEBUG] {method} {resource_path} → {status}", file=sys.stderr)
                        try:
                            # Try to pretty-print the response
                            if hasattr(result, "to_dict"):
                                print(
                                    json.dumps(result.to_dict(), indent=2, default=str),
                                    file=sys.stderr,
                                )
                            elif hasattr(result, "data"):
                                print(
                                    json.dumps(str(result.data)[:2000], indent=2, default=str),
                                    file=sys.stderr,
                                )
                            else:
                                print(repr(result)[:2000], file=sys.stderr)
                        except Exception:
                            print(repr(result)[:2000], file=sys.stderr)

                    return result
                except Exception as exc:
                    # Try to extract status from exception
                    if hasattr(exc, "status"):
                        status = str(exc.status)
                    if DEBUG_ENABLED:
                        import sys

                        print(
                            f"\n[DEBUG] {method} {resource_path} → ERROR {status}: {exc}",
                            file=sys.stderr,
                        )
                    raise
                finally:
                    if TRACE_ENABLED:
                        trace_logger.info(f"API | {method} | {resource_path} | {status} | - | -")

            self.api_client.call_api = traced_call_api

        # V1 APIs
        self.monitors = monitors_api.MonitorsApi(self.api_client)
        self.metrics = metrics_api.MetricsApi(self.api_client)
        self.events = events_api.EventsApi(self.api_client)
        self.hosts = hosts_api.HostsApi(self.api_client)
        self.tags = tags_api.TagsApi(self.api_client)
        self.service_checks = service_checks_api.ServiceChecksApi(self.api_client)
        self.downtimes = downtimes_api.DowntimesApi(self.api_client)
        self.slos = service_level_objectives_api.ServiceLevelObjectivesApi(self.api_client)
        self.dashboards = dashboards_api.DashboardsApi(self.api_client)
        self.usage = usage_metering_api.UsageMeteringApi(self.api_client)
        self.synthetics = synthetics_api.SyntheticsApi(self.api_client)
        self.notebooks = notebooks_api.NotebooksApi(self.api_client)

        # V2 APIs
        self.logs = logs_api.LogsApi(self.api_client)
        self.spans = spans_api.SpansApi(self.api_client)
        self.service_definitions = service_definition_api.ServiceDefinitionApi(self.api_client)
        self.incidents = incidents_api.IncidentsApi(self.api_client)
        self.users = users_api.UsersApi(self.api_client)
        self.rum = rum_api.RUMApi(self.api_client)
        self.ci_pipelines = ci_visibility_pipelines_api.CIVisibilityPipelinesApi(self.api_client)
        self.ci_tests = ci_visibility_tests_api.CIVisibilityTestsApi(self.api_client)
        self.llm_observability = llm_observability_api.LLMObservabilityApi(self.api_client)

        # DBM (direct HTTP — no dedicated SDK module)
        self.dbm = DBMClient(self.api_client)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.api_client.close()


def get_datadog_client() -> DatadogClient:
    """Get configured Datadog client.

    Reads the --profile option from Click context if available.
    """
    import click
    from puppy_kit.config import load_config

    profile = None
    try:
        ctx = click.get_current_context(silent=True)
        if ctx and ctx.obj:
            profile = ctx.obj.get("profile")
    except RuntimeError:
        pass

    config = load_config(profile=profile)
    return DatadogClient(config)
