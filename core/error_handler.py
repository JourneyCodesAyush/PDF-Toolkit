# Centralized error handling

from config.config import setup_logger
import traceback

logger = setup_logger(__name__)


def log_error_with_traceback(exc: Exception, context: str = ""):
    """
    Logs the exception with traceback details using the configured logger
    """

    context_msg = f"Context: {context}" if context else ""
    tb_str = traceback.format_exc()

    log_message = (
        f"Exception occurred: {context_msg}\n"
        f"Exception type: {type(exc).__name__}\n"
        f"Exception message: {exc}\n"
        f"Traceback:\n{tb_str}"
    )
    logger.error(log_message)


def create_msg_object(error_type: str, title: str, message: str) -> dict:
    """
    Creates a dictionary for GUI to consume and display the error or warning
    """

    return {"error_type": error_type, "title": title, "message": message}


def handle_exception(exc: Exception, context: str = "") -> dict:
    """
    Handles exceptions by logging with traceback and returning an error message object for the GUI
    """

    log_error_with_traceback(exc, context)

    if isinstance(exc, FileNotFoundError):
        user_msg = (
            f"The file could not be found {('during ' + context) if context else ''}."
        )
        return create_msg_object("error", "File Not Found Error", user_msg.strip())

    elif isinstance(exc, PermissionError):
        user_msg = f"Permission denied to access the file {('during ' + context) if context else ''}."
        return create_msg_object("error", "Permission Error", user_msg.strip())

    elif isinstance(exc, OSError):
        user_msg = (
            f"An OS error occurred {('during ' + context) if context else ''}: {exc}."
        )
        return create_msg_object("error", "OS Error", user_msg.strip())

    elif isinstance(exc, ValueError):
        user_msg = (
            f"Invalid input provided {('during ' + context) if context else ''}:{exc}"
        )
        return create_msg_object("warning", "Value Error", user_msg.strip())

    else:
        user_msg = f"An unexpected error occurred {('during ' + context) if context else ''}: {exc}"
        return create_msg_object("error", "Unexpected Error", user_msg.strip())
