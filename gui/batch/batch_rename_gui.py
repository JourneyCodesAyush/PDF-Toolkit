# Batch PDF rename GUI


import os
from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from core.batch.batch_rename import batch_rename_pdfs
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def batch_rename_pdf_gui() -> None:
    """
    Handle the GUI workflow for batch renaming PDF files in a selected folder.

    Opens dialogs to select the input folder of PDFs, optionally choose an output folder,
    and prompt the user for a new file name. Calls the core renaming function and displays
    success or error messages accordingly.

    Returns:
        None: This function manages GUI interactions and user messaging, no return value.
    """
    logger.info("Batch rename PDF operation started")

    try:
        input_dir = filedialog.askdirectory(
            title="Select the folder you wish to rename the PDFs of..."
        )

        if not input_dir:
            messagebox.showwarning(
                title="Warning",
                message="Please select a folder whose PDF files you wish to rename.",
            )
            logger.warning(f"Batch renaming failed - No folder selected")
            return

        output_dir_yes_no = messagebox.askyesno(
            title="Output folder",
            message="Do you want to save the merged folder elsewhere?",
        )

        if output_dir_yes_no == True:
            output_dir = filedialog.askdirectory(
                title="Select a directory to save the renamed files"
            )
        else:
            output_dir = input_dir

        new_file_name = simpledialog.askstring(
            title="Rename PDF",
            prompt="Enter the new file name (without .pdf extension)",
        )

        if not new_file_name or not new_file_name.strip():
            messagebox.showwarning(
                title="Warning", message="Please enter a valid file name."
            )
            logger.warning(f"Batch renaming failed - New file name NOT selected")
            return

        new_file_name = new_file_name.strip()

        logger.info(
            f"Batch renaming files inside: {input_dir} -> {os.path.join(output_dir, new_file_name)}"
        )
        result = batch_rename_pdfs(
            input_dir=input_dir, base_name=new_file_name, output_dir=output_dir
        )

        if result.success:
            logger.info(f"Batch renaming successful: {result.message}")
        else:
            logger.warning(
                f"Batch rename operation returned failure message: {result.message}"
            )

        show_message(result)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Renaming PDF")
        show_message(error_msg)
        logger.error(
            f"Batch renaming PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
