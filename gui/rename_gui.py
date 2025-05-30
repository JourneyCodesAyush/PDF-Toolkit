# PDF renaming GUI part here

import os
from config.config import setup_logger
from gui.error_handler_gui import show_message
from core.pdf_rename import rename_pdf_file
from tkinter import messagebox, filedialog, simpledialog

logger = setup_logger(__name__)


def rename_file_gui():
    logger.info("Rename PDF operation started")

    old_file_path = filedialog.askopenfilename(
        title="Select PDF to rename",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )

    if not old_file_path:
        messagebox.showwarning(
            title="Warning", message="Please select a PDF file to rename."
        )
        return

    new_directory = filedialog.askdirectory(
        title="Select a directory to save the renamed file"
    )

    if not new_directory:
        messagebox.showwarning(
            title="Warning", message="Please select a directory to save the file."
        )
        return

    new_file_name = simpledialog.askstring(
        title="Rename PDF", prompt="Enter the new file name (without .pdf extension)"
    )

    if not new_file_name or not new_file_name.strip():
        messagebox.showwarning(
            title="Warning", message="Please enter a valid file name."
        )
        return
    
    new_file_name = new_file_name.strip()

    if not new_file_name.lower().endswith(".pdf"):
        new_file_name += ".pdf"

    result = rename_pdf_file(old_file_path, new_directory, new_file_name)

    show_message(result)

    logger.info(f"Rename operation finished with message: {result['message']}")
