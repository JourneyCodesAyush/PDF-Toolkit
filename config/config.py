# Logging and configuration settings

"""
Logging and configuration settings.

- Sets up basic logging configuration to log INFO and above to a file.
- Provides setup_logger function to create named loggers.
"""

import logging
import os

from config.json_formatter import JsonFormatter
from core.utils import get_app_data_dir

# LOG_FILE_PATH = get_absolute_path("../logs/user_activity.log")
LOG_DIR = get_app_data_dir() / "logs"

# Ensure the logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

USER_LOG_FILE = os.path.join(LOG_DIR, "user_activity.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "errors.ndjson")


logging.basicConfig(
    filename=USER_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# logger = logging.getLogger(__name__)


def setup_logger(name: str = __name__, error_logger: bool = False) -> logging.Logger:
    """
    Create and return a logger instance.
    - If error_only is True, logs only technical errors to errors.log.
    - Otherwise, returns a standard logger that writes to user_activity.log.

    Args:
        name (str): Logger name.
        error_only (bool): Whether to return an error-only logger.

    Returns:
        logging.Logger: Configured logger.
    """

    logger = logging.getLogger(name)

    if error_logger:
        if not any(
            isinstance(h, logging.FileHandler) and h.baseFilename == ERROR_LOG_FILE
            for h in logger.handlers
        ):
            handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8", mode="a")
            handler.setLevel(logging.ERROR)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )
            handler.setFormatter(JsonFormatter())
            logger.addHandler(handler)
            logger.setLevel(logging.ERROR)
            logger.propagate = False

    return logger
