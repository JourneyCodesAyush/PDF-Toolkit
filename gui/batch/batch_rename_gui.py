# Batch PDF rename GUI


import os
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from config.preferences_manager import get_preferences, set_preferences
from core.batch.batch_rename import batch_rename_pdfs
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def batch_rename_pdf_gui(parent_window) -> None:
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

        prefs = get_preferences()
        initial_directory = Path.home()

        if prefs.get("save_preferences") and prefs.get("batch_last_renamed_folder"):
            initial_directory = prefs["batch_last_renamed_folder"]
            initial_directory = Path(str(initial_directory))

        input_dir = filedialog.askdirectory(
            title="Select the folder you wish to rename the PDFs of...",
            initialdir=initial_directory,
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
            message="Do you want to save the renamed files elsewhere?",
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

        def task():
            return batch_rename_pdfs(
                input_dir=input_dir, base_name=new_file_name, output_dir=output_dir
            )

        def on_done(result):
            if result.success:
                logger.info(f"Batch renaming successful: {result.message}")

                # Update the preferences if user opted for it

                if prefs.get("save_preferences"):
                    set_preferences(batch_last_renamed_folder=str(Path(input_dir)))
            else:
                logger.warning(
                    f"Batch rename operation returned failure message: {result.message}"
                )

            show_message(result)

        from gui.common_ui import run_task_with_progress

        run_task_with_progress(root=parent_window, task_func=task, on_done=on_done)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Renaming PDF")
        show_message(error_msg)
        logger.error(
            f"Batch renaming PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
