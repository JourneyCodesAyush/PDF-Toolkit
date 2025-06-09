# GUI window code

import os
from tkinter import Tk, RAISED, Label, Button, Frame
from gui.merge_gui import mergePDF_GUI
from gui.rename_gui import rename_file_gui
from gui.split_gui import split_pdf_gui
from gui.error_handler_gui import show_message
from core.utils import get_absolute_path
from core.result import Result

# from config.config import setup_logger

# logger = setup_logger(__name__)


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
        ICON_PATH = get_absolute_path("assets/PDF_file.ico")
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


def main():
    """
    Initialize and display the main application window for PDF Toolkit.

    The window provides buttons to access PDF merge, rename, and split functionalities.
    Sets up the window layout, fonts, and basic UI components.
    """
    root = Tk()
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(5, weight=1)  # push footer down
    root.title("PDF Toolkit")
    root.geometry("544x344")
    root.resizable(width=False, height=False)

    icon_result = load_icon_safe(root)
    if not icon_result.success and icon_result.error_type == "warning":
        # Show warning if icon fails to load but continue with default icon
        show_message(icon_result)

    TITLE_FONT = ("Helvetica", 16)
    FONT_STYLE = ("Helvetica", 12, "bold")
    BUTTON_FONT = ("Helvetica", 10)

    Label(root, text="PDF Toolkit", font=TITLE_FONT).grid(
        row=0, column=0, columnspan=3, pady=15
    )

    Label(root, text="Want to merge some PDFs?", font=FONT_STYLE).grid(
        row=2, column=1, padx=5, pady=5
    )

    merge_pdf = Button(
        root,
        text="Choose PDFs to merge",
        font=BUTTON_FONT,
        relief=RAISED,
        command=mergePDF_GUI,
    )
    merge_pdf.grid(row=2, column=2, padx=10, pady=10)

    Label(root, text="Want to rename a PDF?", font=FONT_STYLE).grid(
        row=3, column=1, padx=5, pady=5
    )
    rename_pdf = Button(
        root,
        text="Select PDF to rename",
        font=BUTTON_FONT,
        relief=RAISED,
        command=rename_file_gui,
    )
    rename_pdf.grid(row=3, column=2, padx=10, pady=10)

    Label(root, text="Want to split a PDF?", font=FONT_STYLE).grid(
        row=4, column=1, padx=5, pady=5
    )
    split_pdf = Button(
        root,
        text="Choose PDF to split",
        font=BUTTON_FONT,
        relief=RAISED,
        command=split_pdf_gui,
    )
    split_pdf.grid(row=4, column=2, padx=10, pady=10)

    footer_frame = Frame(root, bd=1, relief="sunken")
    footer_frame.grid(row=6, column=0, columnspan=3, pady=(30, 0), sticky="we")

    # Label(footer_frame, text="Version 1.0", font="helvetica 8").pack(
    #     side="right", padx=10
    # )
    Label(footer_frame, text="© 2025 JourneyCodesAyush", font="Helvetica 8").pack(
        side="left", padx=10
    )
    root.mainloop()


if __name__ == "__main__":
    main()
