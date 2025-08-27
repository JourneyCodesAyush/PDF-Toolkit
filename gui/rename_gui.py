# PDF renaming GUI part here

import os
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from config.preferences_manager import get_preferences, set_preferences
from core.error_handler import handle_exception
from core.pdf_rename import rename_pdf_file
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def rename_file_gui(root) -> None:
    """
    GUI handler to rename a PDF file.

    Opens dialogs for the user to select the original PDF,
    choose the output directory, and enter a new file name.
    Calls the core rename function and displays the result.

    Returns:
        None: This function performs GUI interactions and shows messages,
              no return value is needed.
    """
    logger.info("Rename PDF operation started")

    try:

        prefs = get_preferences()
        initial_directory = Path.home()
        if prefs.get("save_preferences") and prefs.get("last_renamed_file"):
            initial_directory = prefs["last_renamed_file"]
            initial_directory = Path(str(initial_directory))

        old_file_path = filedialog.askopenfilename(
            title="Select PDF to rename",
            initialdir=initial_directory,
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )

        if not old_file_path:
            messagebox.showwarning(
                title="Warning", message="Please select a PDF file to rename."
            )
            logger.warning(f"Renaming failed - No PDF file selected")
            return

        new_directory = filedialog.askdirectory(
            title="Select a directory to save the renamed file"
        )

        if not new_directory:
            messagebox.showwarning(
                title="Warning", message="Please select a directory to save the file."
            )
            logger.warning(f"Renaming failed - Output folder NOT selected")
            return

        new_file_name = simpledialog.askstring(
            title="Rename PDF",
            prompt="Enter the new file name (without .pdf extension)",
        )

        if not new_file_name or not new_file_name.strip():
            messagebox.showwarning(
                title="Warning", message="Please enter a valid file name."
            )
            logger.warning(f"Renaming failed - New file name NOT selected")
            return

        new_file_name = new_file_name.strip()

        if not new_file_name.lower().endswith(".pdf"):
            new_file_name += ".pdf"

        logger.info(
            f"Renaming file: {old_file_path} -> {os.path.join(new_directory, new_file_name)}"
        )

        def task():
            return rename_pdf_file(old_file_path, new_directory, new_file_name)

        def on_done(result):
            if result.success:
                logger.info(f"Renaming successful: {result.message}")

                # Update the preferences if user opted for it
                if prefs.get("save_preferences"):
                    set_preferences(last_renamed_file=str(Path(old_file_path).parent))
            else:
                logger.warning(
                    f"Rename operation returned failure message: {result.message}"
                )

            show_message(result)

        from gui.common_ui import run_task_with_progress

        run_task_with_progress(root, task_func=task, on_done=on_done)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Renaming PDF")
        show_message(error_msg)
        logger.error(
            f"Renaming PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
