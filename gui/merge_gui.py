# PDF merging GUI part here

from tkinter import filedialog, messagebox
from core.error_handler import handle_exception
from gui.error_handler_gui import show_message
from core.pdf_merge import mergePDF
from config.config import setup_logger

logger = setup_logger(__name__)


def mergePDF_GUI():
    """
    GUI handler for merging PDFs using core mergePDF function
    """
    logger.info("Merge PDF operation started")

    try:
        input_files = filedialog.askopenfilenames(
            title="Select PDFs to merge",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension="*.pdf",
        )
        if not input_files:
            messagebox.showinfo(
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
            messagebox.showinfo(
                title="No output location selected",
                message="Please provide valid output location",
            )
            logger.warning("Merging failed - Output file name NOT selected")
            return

        result = mergePDF(list(input_files), save_file_path)

        if result.success:
            messagebox.showinfo(title="Success", message=result.message)
            logger.info(f"Merging Successful: {result.message}")
        else:
            show_message(result)
            logger.warning(f"Merging returned failure message: {result.message}")

    except Exception as exc:
        error_msg = handle_exception(exc, context="Merging PDFs")
        show_message(error_msg)
        logger.error(f"Exception during merging: {exc}")
