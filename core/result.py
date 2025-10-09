# Standardized return message from core/ to gui/

from typing import Any


class Result:
    def __init__(
        self,
        success: bool,
        title: str,
        message: str,
        error_type: str | None = None,
        data: dict[str, Any] | None = None,
    ):
        """
        Standardized result object used to return status and messages from core logic to GUI.

        Attributes:
            success (bool): Indicates if the operation was successful.
            title (str): Title to be displayed in the GUI message box.
            message (str): Informational or error message for the user.
            error_type (Optional[str]): Message category - 'error', 'warning', or 'info'.
            data (Optional[Dict[str, Any]]): Additional metadata or context.

        Methods:
            __repr__(): Provides a readable string representation for logging/debugging.
        """

        self.success = success
        self.title = title
        self.message = message
        self.error_type = error_type or ("info" if success else "error")
        self.data = data or {}

    def __repr__(self):
        status = "Success" if self.success else "Failure"
        return f"<Result {status}: {self.error_type.upper()}: {self.title}: {self.message}>"
