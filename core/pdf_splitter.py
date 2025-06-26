# PDF split logic

import os

from PyPDF2 import PdfReader, PdfWriter

from core.error_handler import handle_exception
from core.result import Result
from core.utils import parse_page_ranges, validate_pdf_file


def split_pdf(file_path: str, page_range_input: str, output_dir: str) -> Result:
    """
    Split a PDF file into multiple files based on user-defined page ranges.

    Args:
        file_path (str): Path to the input PDF file.
        page_range_input (str): Page ranges as a string (e.g., "1-3,4,5-7").
        output_dir (str): Directory to save the resulting split PDF files.

    Returns:
        Result: Standardized Result object containing success status, messages,
                and metadata (such as list of created files).
    """
    try:

        if not os.path.isfile(file_path):
            return Result(
                success=False,
                error_type="error",
                title="File Not Found",
                message=f"The original file does not exist: {file_path}",
            )

        if not os.path.isdir(output_dir):
            return Result(
                success=False,
                error_type="error",
                title="Invalid output directory",
                message=f"The specified directory does not exist: {output_dir}",
            )

        if not file_path.lower().endswith(".pdf"):
            # raise ValueError("Selected file is not a PDF.")
            return Result(
                success=False,
                error_type="error",
                title="Invalid file",
                message="Selected file is not a PDF",
            )

        is_valid, error_message = validate_pdf_file(path=file_path)
        if not is_valid:
            return Result(
                success=False,
                error_type="error",
                title="Invalid PDF",
                message=f"{error_message}",
            )

        reader = PdfReader(file_path)
        total_pages = len(reader.pages)

        page_ranges, msg = parse_page_ranges(page_range_input, total_pages)

        if msg:
            return Result(
                success=False,
                error_type="error",
                title="Invalid page range",
                message=msg,
            )

        basename = os.path.splitext(os.path.basename(file_path))[0]

        saved_files = []

        for start, end in page_ranges:
            writer = PdfWriter()
            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])

            if start == end:
                filename = f"{basename}_page_{start}.pdf"
            else:
                filename = f"{basename}_pages_{start}-{end}.pdf"

            output_path = os.path.join(output_dir, filename)

            if os.path.exists(output_path):

                return Result(
                    success=False,
                    error_type="error",
                    title="File Exists",
                    message=f"File '{filename}' already exists in the output directory.",
                )

            with open(output_path, "wb") as out_pdf:
                writer.write(out_pdf)

            saved_files.append(filename)

        return Result(
            success=True,
            error_type="info",
            title="Success",
            message=f"PDF successfully split into {len(page_ranges)} files and saved to {output_dir}.",
            data={"files": saved_files},
        )

    except Exception as e:
        return handle_exception(exc=e, context="Splitting PDF")
