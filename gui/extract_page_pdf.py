# PDF extract page GUI

import os
from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from core.error_handler import handle_exception
from core.pdf_extract_pages import extract_pdf_page
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def extract_page_pdf_gui(root) -> None:
    """
    GUI handler to extract pages from a PDF based on user-specified page range.

    Opens dialogs for selecting an input PDF file, entering page range,
    and choosing an output directory. Delegates the actual extracting
    to the core extract_pdf_page function and handles success or error messaging.

    Returns:
        None: Interacts via GUI dialogs and shows messages; no return value.
    """

    logger.info("Split PDF operation started")
    try:
        file_path = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )

        if not file_path:
            messagebox.showwarning(
                title="No file selected", message="Please select a PDF to split."
            )
            logger.warning("Extracting pages failed - No PDF file selected.")
            return
        page_range_input = simpledialog.askstring(
            title="Page range", prompt="Enter the page range (e.g., 3-7):"
        )

        if not page_range_input or not (page_range_input := page_range_input.strip()):
            messagebox.showwarning(
                title="Invalid Input", message="Please enter a valid page range."
            )
            logger.warning(
                "Extracting pages failed - Page range not provided or empty."
            )
            return

        output_dir = filedialog.askdirectory(
            title="Select folder to save the split files"
        )

        if not output_dir:
            messagebox.showwarning(
                title="No Folder selected", message="Output directory not selected."
            )
            logger.warning("Extracting pages failed - No output folder selected.")
            return

        def task():
            return extract_pdf_page(file_path, page_range_input, output_dir)

        def on_done(result):
            if result.success:
                logger.info(f"{result.message}")
                if result.data and "files" in result.data:
                    for f in result.data["files"]:
                        logger.info(f"Created: {os.path.join(output_dir,f)}")
                logger.info(
                    f"Extract pages from PDF operation finished with message: {result.message}"
                )
            else:
                logger.warning(
                    f"Extract pages from PDF operation returned failure message: {result.message}"
                )

            show_message(result)

        from gui.common_ui import run_task_with_progress

        run_task_with_progress(root, task_func=task, on_done=on_done)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Extracting pages from PDF")
        show_message(error_msg)
        logger.error(
            "Extracting pages from PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
