# Extract page from PDF logic

# PDF extract page logic

import os

from PyPDF2 import PdfReader, PdfWriter

from core.error_handler import handle_exception
from core.result import Result
from core.utils import parse_page_ranges, validate_pdf_file


def extract_pdf_page(file_path: str, page_range_input: str, output_dir: str) -> Result:
    """
    Extract pages from a PDF file based on user-defined page range.

    Args:
        file_path (str): Path to the input PDF file.
        page_range_input (str): Page range as a string (e.g., "1-3").
        output_dir (str): Directory to save the resulting PDF file with extracted pages.

    Returns:
        Result: Standardized Result object containing success status, messages,
                and metadata (such as location of created files).
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
            message=f"Pages {page_ranges} were successfully extracted and saved to {output_dir}.",
            data={"files": saved_files},
        )

    except Exception as e:
        return handle_exception(exc=e, context="Extracting pages from PDF")
