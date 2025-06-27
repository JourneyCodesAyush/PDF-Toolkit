# Batch PDF rename logic

import os
from typing import Optional

from core.error_handler import handle_exception
from core.result import Result
from core.utils import validate_pdf_file


def batch_rename_pdfs(
    input_dir: str, base_name: str, output_dir: Optional[str] = None
) -> Result:
    """
    Rename all PDF files in the input directory with a base name and move them to the output directory.

    Args:
        input_dir (str): Directory containing PDF files to rename.
        base_name (str): Base name for the new PDF files (without '.pdf' extension).
        output_dir (Optional[str]): Directory to save renamed files; defaults to input_dir if not provided.

    Returns:
        Result: Standardized result indicating success or failure, with a descriptive message.
    """
    try:
        if not os.path.isdir(input_dir):
            return Result(
                success=False,
                error_type="error",
                title="Invalid directory",
                message=f"The specified directory does not exist: {input_dir}",
            )

        output_dir = output_dir if output_dir else input_dir

        if not os.path.isdir(output_dir):
            return Result(
                success=False,
                error_type="error",
                title="Invalid directory",
                message=f"The specified directory does not exist: {output_dir}",
            )

        pdf_files = [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.lower().endswith(".pdf")
        ]

        if not pdf_files:
            return Result(
                success=False,
                error_type="error",
                title="Empty directory",
                message=f"No PDF files inside the input directory: {input_dir}",
            )

        if base_name.lower().endswith(".pdf"):
            base_name = base_name[:-4]  # remove extension (.pdf) to append numbers

        for file in pdf_files:
            is_valid, error_message = validate_pdf_file(path=file)
            if not is_valid:
                return Result(
                    success=False,
                    error_type="error",
                    title="Invalid PDF",
                    message=f"{error_message}",
                )

        for i, file in enumerate(pdf_files):
            new_filename = f"{base_name}_{i+1}.pdf"
            new_path = os.path.join(output_dir, new_filename)
            if os.path.exists(new_path):
                return Result(
                    success=False,
                    error_type="error",
                    title="File exists",
                    message=f"A file named '{new_filename}' already exists in the selected directory.",
                )
            os.rename(file, new_path)

        return Result(
            success=True,
            title="Success",
            error_type="info",
            message=f"{len(pdf_files)} PDF files renamed successfully in and/or moved to: {output_dir}.",
        )
    except Exception as e:
        return handle_exception(exc=e, context="Renaming PDFs of a directory")
