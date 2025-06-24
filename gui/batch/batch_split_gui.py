# Batch split PDF GUI


import os
from tkinter import filedialog, simpledialog, messagebox
from config.config import setup_logger
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message
from core.batch.batch_split import batch_split_pdf

logger = setup_logger(__name__)


def batch_split_pdf_gui():
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
        file_path = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )

        if not file_path:
            messagebox.showwarning(
                title="No file selected", message="Please select a PDF to split."
            )
            logger.warning("Splitting failed - No PDF file selected.")
            return

        output_path_yes_no = messagebox.askyesno(
            title="Output folder",
            message="Do you want to save the merged folder elsewhere?",
        )

        if output_path_yes_no:
            output_dir = filedialog.askdirectory(
                title="Where do you want to save the merged file?",
            )
        else:
            output_dir = os.path.dirname(file_path)

        result = batch_split_pdf(file_path, output_dir)
        if result.success:
            logger.info(f"{result.message}")
            if result.data and "files" in result.data:
                for f in result.data["files"]:
                    logger.info(f"Created: {os.path.join(output_dir,f)}")
            logger.info(f"Split operation finished with message: {result.message}")
        else:
            logger.warning(
                f"Split PDF operation returned failure message: {result.message}"
            )

        show_message(result)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Splitting PDF")
        show_message(error_msg)
        logger.error(
            "Splitting PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
