"""Error handling utilities with retry logic."""

from datadog_api_client.exceptions import ApiException
from rich.console import Console
import sys
import time
from functools import wraps
from puppy_kit.utils.exit_codes import (
    AUTH_ERROR,
    GENERAL_ERROR,
    NOT_FOUND,
    RATE_LIMITED,
    SERVER_ERROR,
    VALIDATION_ERROR,
    exit_code_for_status,
)

from puppy_kit.utils.output import emit_error

console = Console()


def handle_api_error(func):
    """Decorator for API error handling with retry logic and LLM-friendly messages."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        retry_delay = 1.0

        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except ApiException as e:
                if e.status == 401:
                    emit_error(
                        "AUTH_FAILED",
                        401,
                        "Authentication failed. Verify DD_API_KEY and DD_APP_KEY are set correctly.",
                        "Run: puppy config test",
                    )
                    sys.exit(AUTH_ERROR)
                elif e.status == 403:
                    emit_error(
                        "PERMISSION_DENIED",
                        403,
                        "Permission denied. Your API key lacks required permissions.",
                        "Check your Datadog API key permissions or run: puppy config test",
                    )
                    sys.exit(AUTH_ERROR)
                elif e.status == 404:
                    emit_error(
                        "NOT_FOUND",
                        404,
                        "Resource not found. The requested ID or resource does not exist.",
                        "Use 'puppy <command> list' to find valid IDs.",
                    )
                    sys.exit(NOT_FOUND)
                elif e.status == 429:
                    # Rate limited - retry with exponential backoff
                    if attempt < retries - 1:
                        wait_time = retry_delay * (2**attempt)
                        console.print(f"[yellow]Rate limited. Retrying in {wait_time}s...[/yellow]")
                        time.sleep(wait_time)
                        continue
                    else:
                        wait_time = retry_delay * (2**retries)
                        suggested_wait = max(wait_time, 30)
                        emit_error(
                            "RATE_LIMITED",
                            429,
                            f"Rate limited by Datadog API after {retries} retries. Suggested wait: {suggested_wait:.0f}+ seconds.",
                            "Try reducing --limit, remove filters, or retry later.",
                        )
                        sys.exit(RATE_LIMITED)
                elif e.status >= 500:
                    # Server error - retry
                    if attempt < retries - 1:
                        console.print(
                            f"[yellow]Server error. Retrying ({attempt + 1}/{retries})...[/yellow]"
                        )
                        time.sleep(retry_delay)
                        continue
                    else:
                        emit_error(
                            "SERVER_ERROR",
                            e.status,
                            "Datadog API server error. The service may be experiencing issues.",
                            "Check https://status.datadoghq.com for incidents. Try again later.",
                        )
                        sys.exit(SERVER_ERROR)
                elif e.status in (400, 422):
                    emit_error(
                        "VALIDATION_ERROR",
                        e.status,
                        f"Validation error ({e.status}). Your request was malformed.",
                        f"Check your query syntax, time ranges, and parameters. Details: {e}",
                    )
                    sys.exit(VALIDATION_ERROR)
                else:
                    emit_error("API_ERROR", e.status, f"API error: {e}")
                    sys.exit(exit_code_for_status(e.status))
            except Exception as e:
                emit_error("UNEXPECTED_ERROR", 0, f"Unexpected error: {e}")
                sys.exit(GENERAL_ERROR)

    return wrapper
