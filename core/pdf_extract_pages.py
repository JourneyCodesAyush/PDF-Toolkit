# Extract page from PDF logic

# PDF extract page logic

import os
from typing import Callable

from PyPDF2 import PdfReader, PdfWriter

from core.error_handler import handle_exception
from core.globals import ENCRYPTED_FILE_HANDLING, EncryptedFileHandling
from core.result import Result
from core.utils import PDFValidationStatus, parse_page_ranges, validate_pdf_file


def extract_pdf_page(
    file_path: str,
    page_range_input: str,
    output_dir: str,
    ask_password_callback: Callable[[str], str | None] | None,
) -> Result:
    """
    Extract pages from a PDF file based on a user-defined page range.

    Supports encrypted PDFs by using a password callback function.

    Args:
        file_path (str): Path to the input PDF file.
        page_range_input (str): Page range as a string (e.g., "1-3", "1,3,5-7").
        output_dir (str): Directory where the extracted pages will be saved.
        ask_password_callback (Callable[[str], str | None] | None):
            A function that accepts the file path and returns the PDF password as a string,
            or None if unavailable. Required for encrypted PDFs.

    Returns:
        Result: A standardized Result object indicating success or failure with appropriate message and metadata.

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

        is_valid, status, error_message = validate_pdf_file(path=file_path)

        password: str | None = None

        if (
            not is_valid and status == PDFValidationStatus.CORRUPTED
        ) or status == PDFValidationStatus.NOT_PDF:
            return Result(
                success=False,
                error_type="error",
                title="Invalid PDF",
                message=f"{error_message}",
            )

        if status == PDFValidationStatus.ENCRYPTED:
            if ask_password_callback is None:
                return Result(
                    success=False,
                    title="Encrypted PDF detected",
                    message="No function to collect the password of the encrypted PDF",
                    error_type="error",
                )

            password = ask_password_callback(file_path)

            if not password:
                if ENCRYPTED_FILE_HANDLING == EncryptedFileHandling.SKIP:
                    return Result(
                        success=False,
                        title="Encrypted PDF detected",
                        message="Current encrypted PDF will be skipped",
                        error_type="info",
                    )
                elif ENCRYPTED_FILE_HANDLING == EncryptedFileHandling.SKIP_ALL:
                    return Result(
                        success=False,
                        title="Encrypted PDF detected",
                        message="All encrypted PDFs will be skipped",
                        error_type="info",
                    )
                return Result(
                    success=False,
                    title="Encrypted PDF detected",
                    message="Encrypted PDF was not given password",
                    error_type="error",
                )

        reader = PdfReader(file_path)

        if reader.is_encrypted:
            if not password:
                return Result(
                    success=False,
                    title="Encrypted PDF detected",
                    message="Password required but not provided or incorrect",
                    error_type="error",
                )
            if reader.decrypt(password) == 0:
                return Result(
                    success=False,
                    title="Wrong Password",
                    message="The provided password for the encrypted PDF is incorrect",
                    error_type="error",
                )

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
        if page_ranges is None:
            return Result(
                success=False,
                error_type="error",
                title="Invalid page range",
                message="Page range cannot be empty",
            )
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
