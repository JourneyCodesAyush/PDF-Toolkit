# JSON file formatter

import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """
    Custom log formatter for JSON output.

    This formatter converts log records into a structured JSON format, which includes
    the timestamp, log level, logger name, message, and additional custom fields like
    context, exception details, and traceback.

    Attributes:
        None directly, as it extends logging.Formatter and overrides the format() method.

    Methods:
        format(record: logging.LogRecord) -> str:
            Converts the log record into a JSON string, including:
            - timestamp: Time when the log entry was created.
            - level: Log level (e.g., 'ERROR', 'INFO').
            - logger: The name of the logger that generated the log.
            - message: The log message.
            - context: Optional custom context for the log.
            - exception_type: Type of the exception.
            - exception_message: The exception's error message.
            - traceback: Full traceback of the exception.
            - exception: The formatted exception string, if exc_info is present in the log.

    Example:
        log_formatter = JsonFormatter()
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(log_formatter)
    """

    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", None),
            "exception_type": getattr(record, "exception_type", None),
            "exception_message": getattr(record, "exception_message", None),
            "traceback": getattr(record, "traceback", None),
        }

        log_record = {
            key: value for key, value in log_record.items() if value is not None
        }

        if record.exc_info:
            log_record["exception"] = super().formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)
