# Batch split PDF GUI


import os
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from config.preferences_manager import get_preferences, set_preferences
from core.batch.batch_split import batch_split_pdf
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def batch_split_pdf_gui(parent_window) -> None:
    """
    Handle the GUI workflow for splitting a PDF into single-page PDFs.

    Opens dialogs to select the input PDF file and choose an output directory,
    then delegates the splitting operation to the core batch_split_pdf function.
    Displays success or error messages based on the outcome.

    Returns:
        None: This function manages GUI dialogs and messaging; it does not return a value.
    """

    logger.info("Batch split PDF operation started")
    try:

        prefs = get_preferences()
        initial_directory = Path.home()

        if prefs.get("save_preferences") and prefs.get("batch_last_split_file"):
            initial_directory = prefs["batch_last_split_file"]
            initial_directory = Path(str(initial_directory))

        file_path = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )

        if not file_path:
            messagebox.showwarning(
                title="No file selected", message="Please select a PDF to split."
            )
            logger.warning("Batch splitting failed - No PDF file selected.")
            return

        output_path_yes_no = messagebox.askyesno(
            title="Output folder",
            message="Do you want to save the splitted PDFs elsewhere?",
        )

        if output_path_yes_no:
            output_dir = filedialog.askdirectory(
                title="Where do you want to save the splitted PDFs?",
            )
        else:
            output_dir = os.path.dirname(file_path)

        def task():
            return batch_split_pdf(file_path, output_dir)

        def on_done(result):
            if result.success:
                logger.info(f"{result.message}")
                if result.data and "files" in result.data:
                    for f in result.data["files"]:
                        logger.info(f"Created: {os.path.join(output_dir,f)}")
                logger.info(
                    f"Batch split operation finished with message: {result.message}"
                )

                # Update the preferences if user opted for it

                if prefs.get("save_preferences"):
                    set_preferences(batch_last_split_file=str(Path(file_path).parent))
            else:
                logger.warning(
                    f"Batch split PDF operation returned failure message: {result.message}"
                )

            show_message(result)

        from gui.common_ui import run_task_with_progress

        run_task_with_progress(root=parent_window, task_func=task, on_done=on_done)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Splitting PDF")
        show_message(error_msg)
        logger.error(
            "Batch splitting PDF failed due to an unexpected error. We are sorry for your inconvenience!"
        )
