# Batch PDF split logic

import os
from typing import Callable

from PyPDF2 import PdfReader, PdfWriter

from core.error_handler import handle_exception
from core.globals import ENCRYPTED_FILE_HANDLING, EncryptedFileHandling
from core.result import Result
from core.utils import PDFValidationStatus, validate_pdf_file


def batch_split_pdf(
    file_path: str,
    output_dir: str | None = None,
    ask_password_callback: Callable[[str], str | None] | None = None,
) -> Result:
    """
    Split a PDF file into multiple single-page PDF files saved in the specified directory.

    Args:
        file_path (str): Path to the input PDF file to be split.
        output_dir (Optional[str]): Directory to save the split PDF files.
            Defaults to the directory of the input file if not provided.

    Returns:
        Result: Standardized Result object indicating success or failure.
            On success, includes a list of the created single-page PDF filenames in 'data'.
    """
    try:
        if not os.path.isfile(file_path):
            return Result(
                success=False,
                error_type="error",
                title="File Not Found",
                message=f"The original file does not exist: {file_path}",
            )

        output_dir = output_dir if output_dir else os.path.dirname(file_path)
        if not os.path.isdir(output_dir):
            return Result(
                success=False,
                error_type="error",
                title="Invalid output directory",
                message=f"The specified directory does not exist: {output_dir}",
            )

        if not file_path.lower().endswith(".pdf"):
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
                    message="Password required but not provided",
                    error_type="error",
                )
            elif reader.decrypt(password) == 0:
                return Result(
                    success=False,
                    title="Wrong Password",
                    message="The provided password for the encrypted PDF is incorrect",
                    error_type="error",
                )

        basename = os.path.splitext(os.path.basename(file_path))[0]

        saved_files = []

        for i, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)

            filename = f"{basename}_page_{i}.pdf"
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
            message=f"PDF successfully split into {len(saved_files)} single-page PDF files and saved to {output_dir}.",
            data={"files": saved_files},
        )

    except Exception as e:
        return handle_exception(exc=e, context="Splitting PDF into single pages")
