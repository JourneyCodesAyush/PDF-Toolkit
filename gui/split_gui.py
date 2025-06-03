# PDF split GUI

import os
from tkinter import filedialog, simpledialog, messagebox
from config.config import setup_logger
from gui.error_handler_gui import show_message
from core.pdf_splitter import split_pdf

logger = setup_logger(__name__)


def split_pdf_gui():
    """
    GUI handler to split a PDF based on user-specified page ranges.
    Invokes file dialogs for input/output and delegates logic to core.
    """

    file_path = filedialog.askopenfilename(
        title="Select PDF to split",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )

    if not file_path:
        messagebox.showwarning(
            title="No file selected", message="Please select a PDF to split."
        )
        logger.warning("No PDF file selected.")
        return
    page_range_input = simpledialog.askstring(
        title="Page ranges", prompt="Enter the page ranges (e.g., 1-3,5,7-9):"
    )

    if not page_range_input or not (page_range_input := page_range_input.strip()):
        messagebox.showwarning(
            title="Invalid Input", message="Please enter a valid page range."
        )
        logger.warning("Page range not provided or empty.")
        return

    output_dir = filedialog.askdirectory(title="Select folder to save the split files")

    if not output_dir:
        messagebox.showwarning(
            title="No Folder selected", message="Output directory not selected."
        )
        logger.warning("No output folder selected.")
        return

    result = split_pdf(file_path, page_range_input, output_dir)
    if result.error_type == "info":
        logger.info(f"{result.message}")
        if result.data and "files" in result.data:
            for f in result.data["files"]:
                logger.info(f"Created: {os.path.join(output_dir,f)}")
        logger.info(f"Split operation finished with message: {result.message}")
    else:
        logger.warning(f"{result.title}: {result.message}")

    show_message(result)
