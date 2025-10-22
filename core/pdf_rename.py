# PDF rename logic

import os

from core.error_handler import handle_exception
from core.result import Result
from core.utils import PDFValidationStatus, validate_pdf_file


def rename_pdf_file(old_path: str, new_directory: str, new_name: str) -> Result:
    """
    Rename a PDF file and move it to a specified directory.

    Args:
        old_path (str): Full path to the original PDF file.
        new_directory (str): Destination directory to save the renamed file.
        new_name (str): New file name for the PDF (must end with .pdf).

    Returns:
        Result: Standardized result object indicating success or failure with message.
    """
    try:
        if not os.path.isfile(old_path):
            return Result(
                success=False,
                error_type="error",
                title="File Not Found",
                message=f"The original file does not exist: {old_path}",
            )

        if not os.path.isdir(new_directory):
            return Result(
                success=False,
                error_type="error",
                title="Invalid directory",
                message=f"The specified directory does not exist: {new_directory}",
            )

        if not old_path.lower().endswith(".pdf"):
            # raise ValueError("Selected file is not a PDF.")
            return Result(
                success=False,
                error_type="error",
                title="Invalid file",
                message="Selected file not a PDF",
            )

        if not new_name or not new_name.strip():
            return Result(
                success=False,
                error_type="Error",
                title="New file name not selected",
                message="New file name for the pdf is empty",
            )

        if not new_name.lower().endswith(".pdf"):
            # raise ValueError("New file name must have a .pdf extension.")
            new_name += ".pdf"

        is_valid, status, error_message = validate_pdf_file(path=old_path)

        if (
            not is_valid and status == PDFValidationStatus.CORRUPTED
        ) or status == PDFValidationStatus.NOT_PDF:
            return Result(
                success=False,
                error_type="error",
                title="Invalid PDF",
                message=f"{error_message}",
            )

        new_path = os.path.join(new_directory, new_name)

        if os.path.exists(new_path):
            return Result(
                success=False,
                error_type="error",
                title="File exists",
                message=f"A file named '{new_path}' already exists in the selected directory.",
            )

        os.rename(old_path, new_path)
        return Result(
            success=True,
            title="Success",
            error_type="info",
            message=f"File renamed to '{new_name}' and moved to selected directory.",
        )
    except Exception as e:
        return handle_exception(exc=e, context="renaming PDF")
