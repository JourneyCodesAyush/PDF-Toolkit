# PDF merge logic

from PyPDF2 import PdfMerger
from core import error_handler
from core.result import Result


def mergePDF(input_file_path: list[str], output_file_path: str) -> Result:
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
        # return success_failure("Failure", message="No input files selected")

    merger = PdfMerger()
    try:
        for pdf in input_file_path:
            if not pdf.lower().endswith(".pdf"):
                # success_failure("Failure", message=ValueError)
                raise ValueError(f"Invalid file format (not a PDF): {pdf}")
            merger.append(pdf)
        merger.write(output_file_path)
        return Result(
            success=True,
            title="Success",
            message="PDFs merged successfully!",
            error_type="info",
        )
        # return success_failure("Success", "PDFs merged successfully!")
    except Exception as e:
        return error_handler.handle_exception(exc=e, context="merging PDFs")
        # return success_failure("Failure", message=str(e))

    finally:
        merger.close()
