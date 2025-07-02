# Batch PDF merge GUI logic


from tkinter import filedialog, messagebox, simpledialog

from config.config import setup_logger
from core.batch.batch_merge import batch_merge_pdfs
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def batch_merge_pdf_gui(parent_window) -> None:
    """
    Handle the GUI workflow for merging multiple PDF files into one.

    Opens dialogs for the user to select the input folder containing PDFs,
    prompts for an optional output folder to save the merged PDF,
    then asks for a new name for the merged file (without the .pdf extension),
    then calls the core batch merge function and displays success or error messages.

    Returns:
        None: This function manages GUI interactions and user messaging, no return value.
    """
    logger.info("Batch merge PDF operation started")

    try:

        input_dir = filedialog.askdirectory(
            title="Select the folder you wish to merge the PDFs of."
        )

        if not input_dir:
            messagebox.showwarning(
                title="No directory selected",
                message="No input directory was selected!",
            )
            logger.warning(f"Batch merge failed - No folder selected")
            return

        output_path_yes_no = messagebox.askyesno(
            title="Output folder",
            message="Do you want to save the merged PDF elsewhere?",
        )

        if output_path_yes_no:
            output_dir = filedialog.askdirectory(
                title="Where do you want to save the merged file?",
            )
        else:
            output_dir = input_dir

        new_name = simpledialog.askstring(
            title="New PDF name",
            prompt="Enter the name for the merged PDF(without .pdf extension)",
        )

        if not new_name.endswith(".pdf"):
            new_name += ".pdf"

        def task():
            return batch_merge_pdfs(
                input_dir_path=input_dir, new_name=new_name, output_dir=output_dir
            )

        def on_done(result):
            if result.success:
                logger.info(
                    f"Batch merged files of {input_dir} to {output_dir}/{new_name}"
                )
                logger.info(f"Batch merging successful: {result.message}")
            else:
                logger.warning(
                    f"Batch merge returned failure message: {result.message}"
                )

            show_message(result)

        from gui.common_ui import run_task_with_progress

        run_task_with_progress(root=parent_window, task_func=task, on_done=on_done)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Merging PDFs")
        show_message(error_msg)
        logger.error(
            "Batch merging PDFs failed due to an unexpected error. We are sorry for your inconvenience!"
        )
