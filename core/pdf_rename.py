# PDF rename logic

import os
from core.error_handler import handle_exception, create_msg_object
from core.result import Result


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
        if not old_path.lower().endswith(".pdf"):
            raise ValueError("Selected file is not a PDF.")
        if not new_name.lower().endswith(".pdf"):
            raise ValueError("New file name must have a .pdf extension.")

        new_path = os.path.join(new_directory, new_name)

        if os.path.exists(new_path):
            return create_msg_object(
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
        return handle_exception(e, context="renaming PDF")
