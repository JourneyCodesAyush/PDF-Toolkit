# Batch PDF merge logic

import os
from typing import Optional

from PyPDF2 import PdfMerger

from core.error_handler import handle_exception
from core.result import Result
from core.utils import validate_pdf_file


def batch_merge_pdfs(
    input_dir_path: str, new_name: str, output_dir: str | None
) -> Result:
    """
    Merge multiple PDF files from a directory into a single PDF saved to the specified path.

    Args:
        input_dir_path (str): Path to the directory containing PDF files to merge.
        new_name (str): The name of the merged output PDF file (without a '.pdf' extension).
        output_dir (Optional[str]): Path where the merged PDF will be saved.
            If None, defaults to input directory path.

    Returns:
        Result: Object indicating success or failure, with relevant message and error type.
    """

    if not input_dir_path:
        return Result(
            success=False, title="No files", message="No input files selected."
        )

    if not new_name or new_name.strip() == "":
        return Result(
            success=False,
            title="Invalid name",
            message="Name of the merged PDF cannot be empty",
        )

    output_dir = output_dir if output_dir else input_dir_path

    if os.path.abspath(os.path.join(output_dir, new_name)) in [
        os.path.abspath(p) for p in os.path.join(output_dir, new_name)
    ]:
        return Result(
            success=False,
            title="Invalid output path",
            message="Output file path cannot be same as any input file.",
        )

    if os.path.exists(os.path.join(output_dir, new_name)):
        return Result(
            success=False, title="Duplicate file", message="Location already exists."
        )

    pdf_files = [
        os.path.join(input_dir_path, f)
        for f in os.listdir(input_dir_path)
        if f.lower().endswith(".pdf")
    ]

    if not new_name.endswith(".pdf"):
        new_name += ".pdf"

    merger = PdfMerger()
    try:
        for pdf in pdf_files:
            is_valid, error_message = validate_pdf_file(path=pdf)
            if not is_valid:
                # raise ValueError(f"{error_message}")
                return Result(
                    success=False,
                    error_type="error",
                    title="Invalid file",
                    message=f"{error_message}",
                )

            merger.append(pdf)
        merger.write(os.path.join(output_dir, new_name))
        return Result(
            success=True,
            title="Success",
            message="PDFs merged successfully!",
            error_type="info",
        )

    except Exception as e:
        return handle_exception(exc=e, context="Merging PDFs of a directory")

    finally:
        merger.close()
