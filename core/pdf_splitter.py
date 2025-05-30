# PDF split logic

import os
from PyPDF2 import PdfReader, PdfWriter
from core.utils import parse_page_ranges
from core.error_handler import handle_exception
from config.config import setup_logger

logger = setup_logger(__name__)


def split_pdf(file_path: str, page_range_input: str, output_dir: str) -> dict:
    """
    Split a PDF file by given page ranges and save output files.

    Args:
        file_path (str): Input PDF file path
        page_range_input (str): User input for pages, e.g. "1-3,4,5-7"
        output_dir (str): Directory to save split files

    Returns:
        dict: A message dict (error_type, title, message) for GUI
    """
    try:

        if not file_path.lower().endswith(".pdf"):
            raise ValueError("Selected file is not a PDF.")

        reader = PdfReader(file_path)
        total_pages = len(reader.pages)

        page_ranges = parse_page_ranges(page_range_input, total_pages)

        basename = os.path.splitext(os.path.basename(file_path))[0]

        split_count = 0

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
                logger.warning(f"File already exists: {output_path}")
                return {
                    "error_type": "error",
                    "title": "File Exists",
                    "message": f"File '{filename}' already exists in the output directory.",
                }

            with open(output_path, "wb") as out_pdf:
                writer.write(out_pdf)
            logger.info(f"Saved split PDF: {output_path}")
            split_count += 1

        logger.info(f"{split_count} PDF file(s) saved to: {output_dir}")
        return {
            "error_type": "info",
            "title": "Success",
            "message": f"PDF successfully split into {len(page_ranges)} files and saved to {output_dir}.",
        }

    except Exception as e:
        return handle_exception(e, context="Splitting PDF")
