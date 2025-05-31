# Standardized return message from core/ to gui/

from typing import Optional


class Result:
    def __init__(
        self,
        success: bool,
        title: str,
        message: str,
        error_type: Optional[str] = None,
        data: Optional[str] = None,
    ):
        """
        Standard result message from core to GUI.

        Args:
            success (bool): Whether the operation was successful.
            title (str): Title for the message box.
            message (str): Main text message for the user.
            error_type (Optional[str]): 'error', 'warning', or 'info' (used by GUI).
            data (Optional[dict]): Any additional metadata.
        """
        self.success = success
        self.title = title
        self.message = message
        self.error_type = error_type or ("info" if success else "error")
        self.data = data or {}

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "title": self.title,
            "message": self.message,
            "error_type": self.error_type,
            **self.data,
        }

    def __repr__(self):
        return f"<Result {self.error_type.upper()}: {self.title}: {self.message}>"
