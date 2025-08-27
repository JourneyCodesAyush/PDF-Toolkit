# PDF split GUI

import os
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from config.preferences_manager import get_preferences, set_preferences
from core.error_handler import handle_exception
from core.pdf_splitter import split_pdf
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def split_pdf_gui(root) -> None:
    """
    GUI handler to split a PDF based on user-specified page ranges.

    Opens dialogs for selecting an input PDF file, entering page ranges,
    and choosing an output directory. Delegates the actual splitting
    to the core split_pdf function and handles success or error messaging.

    Returns:
        None: Interacts via GUI dialogs and shows messages; no return value.
    """

    logger.info("Split PDF operation started")
    try:

        prefs = get_preferences()
        initial_directory = Path.home()
        if prefs.get("save_preferences") and prefs.get("last_split_file"):
            initial_directory = prefs["last_split_file"]
            initial_directory = Path(str(initial_directory))

        file_path = filedialog.askopenfilename(
            title="Select PDF to split",
            initialdir=initial_directory,
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )

        if not file_path:
            messagebox.showwarning(
                title="No file selected", message="Please select a PDF to split."
            )
            logger.warning("Splitting failed - No PDF file selected.")
            return
        page_range_input = simpledialog.askstring(
            title="Page ranges", prompt="Enter the page ranges (e.g., 1-3,5,7-9):"
        )

        if not page_range_input or not (page_range_input := page_range_input.strip()):
            messagebox.showwarning(
                title="Invalid Input", message="Please enter a valid page range."
            )
            logger.warning("Splitting failed - Page range not provided or empty.")
            return

        output_dir = filedialog.askdirectory(
            title="Select folder to save the split files"
        )

        if not output_dir:
            messagebox.showwarning(
                title="No Folder selected", message="Output directory not selected."
            )
            logger.warning("Splitting failed - No output folder selected.")
            return

        def task():
            return split_pdf(file_path, page_range_input, output_dir)

        def on_done(result):
            if result.success:
                logger.info(f"{result.message}")
                if result.data and "files" in result.data:
                    for f in result.data["files"]:
                        logger.info(f"Created: {os.path.join(output_dir,f)}")
                logger.info(f"Split operation finished with message: {result.message}")

                # Update the preferences if user opted for it

                if prefs.get("save_preferences"):
                    set_preferences(last_split_file=str(Path(file_path).parent))
            else:
                logger.warning(
                    f"Split PDF operation returned failure message: {result.message}"
                )

            show_message(result)

        from gui.common_ui import run_task_with_progress

        run_task_with_progress(root, task_func=task, on_done=on_done)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Splitting PDF")
        show_message(error_msg)
        logger.error(
            "Splitting PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
