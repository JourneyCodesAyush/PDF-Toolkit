# Batch PDF merge GUI logic


from tkinter import filedialog, messagebox, simpledialog
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message
from core.batch.batch_merge import batch_merge_pdfs
from config.config import setup_logger

logger = setup_logger(__name__)


def batch_merge_pdf_gui():
    """
    GUI handler to merge multiple PDF files into a single PDF.

    Opens file dialogs for user to select directory of PDFs to merge,
    prompts for output save location, calls the core merge function,
    and displays success or error messages.

    Returns:
        None: This function performs GUI interactions and shows messages,
              no return value is needed.
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
            message="Do you want to save the merged folder elsewhere?",
        )

        if output_path_yes_no:
            save_file_path = filedialog.askdirectory(
                title="Where do you want to save the merged file?",
            )
        else:
            save_file_path = input_dir

        result = batch_merge_pdfs(input_dir, save_file_path)

        if result.success:
            logger.info(f"Batch merging successful: {result.message}")
        else:
            logger.warning(f"Batch merge returned failure message: {result.message}")

        show_message(result)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Merging PDFs")
        show_message(error_msg)
        logger.error(
            "Batch merging PDFs failed due to an unexpected error. We are sorry for your inconvenience!"
        )
