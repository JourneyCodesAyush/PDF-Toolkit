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
    Rename a PDF file and move it to a specified directory.

    Args:
        input_dir (str):  Directory containing PDF files to rename.
        output_dir (str): Destination directory to save the renamed files.
        base_name (str): New file name for the PDF files (Should NOT include .pdf extension).

    Returns:
        Result: Standardized result object indicating success or failure with message.
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
            message=f"{len(pdf_files)} PDF files renamed successfully to: {output_dir}.",
        )
    except Exception as e:
        return handle_exception(exc=e, context="Renaming PDFs of a directory")
 