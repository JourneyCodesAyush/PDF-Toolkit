# GUI window code

import os
from tkinter import RAISED, Button, Frame, Label, Tk

from core.result import Result
from core.utils import get_absolute_path
from gui.batch.batch_operations_gui import batch_operations_gui_window
from gui.common_ui import load_icon_safe
from gui.error_handler_gui import show_message
from gui.merge_gui import mergePDF_GUI
from gui.rename_gui import rename_file_gui
from gui.split_gui import split_pdf_gui
from version import __version__

# from config.config import setup_logger

# logger = setup_logger(__name__)


def main() -> None:
    """
    Initialize and display the main application window for PDF Toolkit.

    The window provides buttons to access PDF merge, rename, and split functionalities.
    Sets up the window layout, fonts, and basic UI components.
    """
    root = Tk()
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(5, weight=1)  # push footer down
    root.title(f"PDF Toolkit v{__version__}")
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

    Label(root, text="Need to process multiple PDFs?", font=FONT_STYLE).grid(
        row=5, column=1, padx=5, pady=5
    )

    batch_button = Button(
        root,
        text="Batch Operations",
        font=BUTTON_FONT,
        relief=RAISED,
        command=lambda: batch_operations_gui_window(root),
    )
    batch_button.grid(row=5, column=2, padx=10, pady=10)

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
