# Shared UI

import os
from core.result import Result
from core.utils import get_absolute_path

def load_icon_safe(root) -> Result:
    """
    Safely attempts to load and set the application icon for the given Tkinter root window.

    Args:
        root (Tk): The Tkinter root window instance where the icon will be set.

    Returns:
        Result: A Result object indicating whether the icon was successfully loaded.

    Behavior:
        Tries to locate the icon file using an absolute path. If found, sets it as the window icon.
        If the icon file is missing or cannot be loaded, returns a warning Result with the error details.
    """
    try:
        # ICON_PATH = get_absolute_path("../assets/PDF_file.ico")
        ICON_PATH = get_absolute_path(os.path.join("assets", "PDF_file.ico"))
        if not os.path.exists(ICON_PATH):
            raise FileNotFoundError(f"Icon not found at: {ICON_PATH}")
        root.iconbitmap(ICON_PATH)
        return Result(
            success=True,
            title="Icon Loaded",
            message="App Icon loaded successfully.",
            error_type="info",
        )
    except Exception as e:
        return Result(
            success=False,
            title="Icon load failed",
            message=f"Could not load app icon.\nUsing default icon.\n\nDetails: {str(e)}",
            error_type="warning",
        )

