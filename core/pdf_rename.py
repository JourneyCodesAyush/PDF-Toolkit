# PDF rename logic

import os
from core.error_handler import handle_exception, create_msg_object
from core.result import Result


def rename_pdf_file(old_path: str, new_directory: str, new_name: str) -> Result:
    """
    Renames a PDF file and moves it to a new directory

    Args:
        old_path (str): The full path to the original PDF file.
        new_directory (str): The directory where the renamed file will be saved.
        new_name (str): The new name for the PDF file.

    Returns:
        Result: A standardized Result object for GUI display.

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
