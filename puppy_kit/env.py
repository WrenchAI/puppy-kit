"""
Environment variable configuration for puppy-kit.

Supported variables:
  PUPPY_KIT_TRACE=true   — Write pipe-delimited trace log of all CLI invocations and API calls
  PUPPY_KIT_DEBUG=true   — Print raw API responses to stderr for debugging
"""

import os


def _bool_env(name: str) -> bool:
    """Parse boolean environment variable."""
    return os.environ.get(name, "").lower() == "true"


TRACE_ENABLED: bool = _bool_env("PUPPY_KIT_TRACE")
DEBUG_ENABLED: bool = _bool_env("PUPPY_KIT_DEBUG")
