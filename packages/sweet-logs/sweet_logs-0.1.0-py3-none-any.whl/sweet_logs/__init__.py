"""Top-level package for Sweet Logs."""

__version__ = "0.1.0"

from sweet_logs import config, formatters  # noqa: F401
from sweet_logs.hooks import local_log_safe, log_critical_hook  # noqa: F401
from sweet_logs.setup import setup_logging  # noqa: F401
