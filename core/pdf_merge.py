# PDF merge logic

from PyPDF2 import PdfMerger
from core import error_handler


def success_failure(result: str, message: str) -> dict:
    return {"result": result, "message": message}


def mergePDF(input_file_path: list[str], output_file_path: str):
    """
    Takes the list of locations of PDFs
    Saves the file at outpath
    """

    if not input_file_path:
        success_failure("Failure", message=ValueError)
        raise ValueError("No input files selected")

    merger = PdfMerger()
    try:
        for pdf in input_file_path:
            if not pdf.lower().endswith(".pdf"):
                # success_failure("Failure", message=ValueError)
                raise ValueError(f"Invalid file format (not a PDF): {pdf}")
            merger.append(pdf)
        merger.write(output_file_path)
        return success_failure("success", "PDFs merged successfully!")
    finally:
        merger.close()
