import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from puppy_kit.commands.config import get_config_dir
from puppy_kit.env import TRACE_ENABLED, DEBUG_ENABLED

try:
    from puppy_kit._version import __version__
except ImportError:
    __version__ = "0.0.0-dev"


trace_logger = logging.getLogger("puppy_kit.trace")
trace_logger.propagate = False

if TRACE_ENABLED and not trace_logger.handlers:
    trace_path = Path(get_config_dir(), ".puppy_kit_trace.log")
    handler = RotatingFileHandler(
        trace_path,
        mode="a",
        encoding="utf-8",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d | %H:%M:%S")
    )
    trace_logger.addHandler(handler)
    trace_logger.setLevel(logging.INFO)


__all__ = ["TRACE_ENABLED", "DEBUG_ENABLED", "trace_logger", "__version__"]
