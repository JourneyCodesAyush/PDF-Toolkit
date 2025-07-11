# PDF merge logic

from PyPDF2 import PdfMerger

from core.error_handler import handle_exception
from core.result import Result
from core.utils import validate_pdf_file


def merge_pdf(input_file_path: list[str], output_file_path: str) -> Result:
    """
    Merge multiple PDF files into a single PDF saved at the specified output path.

    Args:
        input_file_path (list[str]): List of input PDF file paths to merge.
        output_file_path (str): Output file path for the merged PDF.

    Returns:
        Result: Standardized result object indicating success or failure with message.
    """

    if not input_file_path:
        return Result(
            success=False, title="No files", message="No input files selected."
        )

    merger = PdfMerger()
    try:
        for pdf in input_file_path:
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
        merger.write(output_file_path)
        return Result(
            success=True,
            title="Success",
            message="PDFs merged successfully!",
            error_type="info",
        )

    except Exception as e:
        return handle_exception(exc=e, context="merging PDFs")

    finally:
        merger.close()
