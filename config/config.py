# Logging and configuration settings

import logging

LOG_FILE_PATH = "logs/user_activity.log"

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# logger = logging.getLogger(__name__)


def setup_logger(name: str = __name__):
    return logging.getLogger(name)
