# Logging and configuration settings

"""
Logging and configuration settings.

- Sets up basic logging configuration to log INFO and above to a file.
- Provides `setup_logger` function to create named loggers.
"""

import logging
import os
from core.utils import get_absolute_path

LOG_FILE_PATH = get_absolute_path("../logs/user_activity.log")

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# logger = logging.getLogger(__name__)


def setup_logger(name: str = __name__):
    """
    Returns a logger with the specified name.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
