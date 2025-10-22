# PDF merge logic

import os
from pathlib import Path
from typing import Callable

from PyPDF2 import PdfMerger, PdfReader

from core.error_handler import handle_exception
from core.globals import ENCRYPTED_FILE_HANDLING, EncryptedFileHandling
from core.result import Result
from core.utils import PDFValidationStatus, validate_pdf_file


def merge_pdf(
    input_file_path: list[str],
    output_file_path: str,
    ask_password_callback: Callable[[str], str | None] | None,
) -> Result:
    """
    Merge multiple PDF files into a single output PDF.

    This function combines multiple PDF files into one. It handles encrypted PDFs
    based on global settings and an optional password callback. Files that are
    invalid, corrupted, or provided with incorrect passwords are skipped and
    reported.

    Args:
        input_file_path (list[str]):
            List of paths to input PDF files to be merged.

        output_file_path (str):
            Destination file path for the merged PDF. Must not already exist and
            must not overlap with input files.

        ask_password_callback (Callable[[str], str | None] | None):
            Optional callback to provide passwords for encrypted PDFs.
            If not provided, encrypted PDFs will be skipped unless global handling
            allows silent skipping.

    Returns:
        Result: A standardized Result object indicating success or failure, along with an appropriate title and metadata.
    """

    if not input_file_path:
        return Result(
            success=False, title="No files", message="No input files selected."
        )

    if not output_file_path or output_file_path.strip() == "":
        return Result(
            success=False,
            title="Invalid output path",
            message="Output file path cannot be empty.",
        )

    if os.path.abspath(output_file_path) in [
        os.path.abspath(p) for p in input_file_path
    ]:
        return Result(
            success=False,
            title="Invalid output path",
            message="Output file path cannot be same as any input file.",
        )

    if os.path.exists(output_file_path):
        return Result(
            success=False, title="Duplicate file", message="Location already exists."
        )

    invalid_files: list[str] = []
    wrong_password_files: list[str] = []
    skipped_encrypted_files: list[str] = []

    merger = PdfMerger()
    try:
        for pdf in input_file_path:
            is_valid, status, error_message = validate_pdf_file(path=pdf)

            password: str | None = None

            # PDF is not valid AND it is corrupted or it is NOT a PDF
            if (
                not is_valid and status == PDFValidationStatus.CORRUPTED
            ) or status == PDFValidationStatus.NOT_PDF:
                invalid_files.append(pdf)
                continue

            # PDF is valid but encrypted
            if status == PDFValidationStatus.ENCRYPTED:
                # If user chooses to skip all the encrypted PDFs, then don't call the callback function

                if ENCRYPTED_FILE_HANDLING == EncryptedFileHandling.SKIP_ALL:
                    skipped_encrypted_files.append(pdf)
                    continue

                # Check if a callback function is provided or not
                if ask_password_callback is None:
                    skipped_encrypted_files.append(pdf)
                    continue

                password = ask_password_callback(pdf)

                # If user chooses to skip the file, leave it
                if ENCRYPTED_FILE_HANDLING == EncryptedFileHandling.SKIP:
                    continue

                # Password not provided, return
                if not password:
                    wrong_password_files.append(pdf)
                    continue

            reader = PdfReader(pdf)

            if reader.is_encrypted and password is not None:
                decrypt_result: int = reader.decrypt(password=password)
                if decrypt_result == 0:
                    wrong_password_files.append(pdf)
                    continue

            merger.append(reader)
        merger.write(output_file_path)

        notes: list[str] = []

        if skipped_encrypted_files:
            skipped_names: str = ", ".join(
                Path(f).name for f in skipped_encrypted_files
            )
            notes.append(f"Skipped encrypted PDFs: {skipped_names}")

        if wrong_password_files:
            wrong_pw_names: str = ", ".join(Path(f).name for f in wrong_password_files)
            notes.append(f"PDFs with wrong passwords: {wrong_pw_names}")

        if invalid_files:
            invalid_names = ", ".join(Path(f).name for f in invalid_files)
            notes.append(f"Invalid PDFs: {invalid_names}")

        return Result(
            success=True,
            title="Success",
            message="PDFs merged successfully!",
            error_type="info",
            data={
                "invalid_files": invalid_files,
                "skipped_encrypted_files": skipped_encrypted_files,
                "wrong_password_files": wrong_password_files,
            },
        )

    except Exception as e:
        return handle_exception(exc=e, context="merging PDFs")

    finally:
        merger.close()
