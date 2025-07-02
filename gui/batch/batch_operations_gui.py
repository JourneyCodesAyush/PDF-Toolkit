# Batch Operations GUI

from tkinter import RAISED, Button, Frame, Label, Toplevel

from core.result import Result
from gui.batch.batch_merge_gui import batch_merge_pdf_gui
from gui.batch.batch_rename_gui import batch_rename_pdf_gui
from gui.batch.batch_split_gui import batch_split_pdf_gui
from gui.common_ui import load_icon_safe
from gui.error_handler_gui import show_message
from version import __version__


def batch_operations_gui_window(parent=None) -> None:
    """
    Create and display the Batch Operations window as a Tkinter Toplevel.

    Sets up UI elements including buttons for batch PDF merge, rename, and split operations,
    configures window properties, and handles loading the application icon.

    Args:
        parent (tk.Widget, optional): The parent widget for this window. Defaults to None.

    Returns:
        None: This function creates and manages the window, it does not return a value.
    """

    window = Toplevel(parent)
    window.transient(parent)
    window.grab_set()
    window.focus_set()
    window.lift()
    for i in range(3):
        window.grid_columnconfigure(i, weight=1)
    window.grid_rowconfigure(5, weight=1)  # push footer down
    window.title(f"PDF Toolkit v{__version__}")
    window.geometry("544x344")
    icon_result = load_icon_safe(window)
    if not icon_result.success and icon_result.error_type == "warning":
        show_message(icon_result)

    TITLE_FONT = ("Helvetica", 16)
    FONT_STYLE = ("Helvetica", 12, "bold")
    BUTTON_FONT = ("Helvetica", 10)

    Label(window, text="PDF Toolkit - Batch Operations", font=TITLE_FONT).grid(
        row=0, column=0, columnspan=3, pady=15
    )

    Label(window, text="Want to merge PDFs of an entire folder?", font=FONT_STYLE).grid(
        row=2, column=1, padx=5, pady=5
    )

    merge_pdf = Button(
        window,
        text="Select the folder",
        font=BUTTON_FONT,
        relief=RAISED,
        command= lambda: batch_merge_pdf_gui(window),
    )
    merge_pdf.grid(row=2, column=2, padx=10, pady=10)

    Label(window, text="Want to rename PDFs of a folder?", font=FONT_STYLE).grid(
        row=3, column=1, padx=5, pady=5
    )
    rename_pdf = Button(
        window,
        text="Select the folder",
        font=BUTTON_FONT,
        relief=RAISED,
        command= lambda: batch_rename_pdf_gui(window),
    )
    rename_pdf.grid(row=3, column=2, padx=10, pady=10)

    Label(
        window, text="Want to split a PDF into single-paged ones?", font=FONT_STYLE
    ).grid(row=4, column=1, padx=5, pady=5)
    split_pdf = Button(
        window,
        text="Choose PDF to split",
        font=BUTTON_FONT,
        relief=RAISED,
        command= lambda: batch_split_pdf_gui(window),
    )
    split_pdf.grid(row=4, column=2, padx=10, pady=10)

    footer_frame = Frame(window, bd=1, relief="sunken")
    footer_frame.grid(row=6, column=0, columnspan=3, pady=(30, 0), sticky="we")

    # Label(footer_frame, text="Version 1.0", font="helvetica 8").pack(
    #     side="right", padx=10
    # )
    Label(footer_frame, text="© 2025 JourneyCodesAyush", font="Helvetica 8").pack(
        side="left", padx=10
    )


if __name__ == "__main__":
    batch_operations_gui_window()
