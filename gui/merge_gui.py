# PDF merging GUI part here

from tkinter import filedialog, messagebox

from config.config import setup_logger
from core.error_handler import handle_exception
from core.pdf_merge import merge_pdf
from gui.error_handler_gui import show_message

logger = setup_logger(__name__)


def merge_pdf_gui() -> None:
    """
    GUI handler to merge multiple PDF files into a single PDF.

    Opens file dialogs for user to select multiple PDFs to merge,
    prompts for output save location, calls the core merge function,
    and displays success or error messages.

    Returns:
        None: This function performs GUI interactions and shows messages,
              no return value is needed.
    """
    logger.info("Merge PDF operation started")

    try:
        input_files = filedialog.askopenfilenames(
            title="Select PDFs to merge",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )
        if not input_files:
            messagebox.showwarning(
                title="No files selected", message="No PDF files selected!"
            )
            logger.warning("Merging failed - No file selected")
            return

        save_file_path = filedialog.asksaveasfilename(
            title="Where do you want to save the file?",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension=".pdf",
        )

        if not save_file_path:
            messagebox.showwarning(
                title="No output location selected",
                message="Please provide valid output location",
            )
            logger.warning("Merging failed - Output file name NOT selected")
            return

        result = merge_pdf(list(input_files), save_file_path)

        if result.success:
            logger.info(
                f"Merged files: { ', '.join([input_file for input_file in input_files])} to {save_file_path}"
            )
            logger.info(f"Merging Successful: {result.message}")
        else:
            logger.warning(f"Merge returned failure message: {result.message}")

        show_message(result)

    except Exception as exc:
        error_msg = handle_exception(exc, context="Merging PDFs")
        show_message(error_msg)
        logger.error(
            "Merging PDFs failed due to an unexpected error. We are sorry for your inconvenience!"
        )
