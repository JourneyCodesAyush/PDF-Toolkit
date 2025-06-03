# PDF split logic

import os
from PyPDF2 import PdfReader, PdfWriter
from core.utils import parse_page_ranges
from core.error_handler import handle_exception
from core.result import Result


def split_pdf(file_path: str, page_range_input: str, output_dir: str) -> Result:
    """
    Split a PDF file by given page ranges and save output files.

    Args:
        file_path (str): Input PDF file path
        page_range_input (str): User input for pages, e.g. "1-3,4,5-7"
        output_dir (str): Directory to save split files

    Returns:
        Result: Standardized result object with status and message for GUI consumption.
    """
    try:

        if not file_path.lower().endswith(".pdf"):
            raise ValueError("Selected file is not a PDF.")

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
        return handle_exception(e, context="Splitting PDF")
