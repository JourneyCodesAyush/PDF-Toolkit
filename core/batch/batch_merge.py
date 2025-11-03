# Batch PDF merge logic

import os
from pathlib import Path
from typing import Callable

from PyPDF2 import PdfMerger, PdfReader

from core.error_handler import handle_exception
from core.globals import ENCRYPTED_FILE_HANDLING, EncryptedFileHandling
from core.result import Result
from core.utils import PDFValidationStatus, validate_pdf_file


def batch_merge_pdfs(
    input_dir_path: str,
    new_name: str,
    output_dir: str | None,
    ask_password_callback: Callable[[str], str | None] | None,
) -> Result:
    """
    Merge multiple PDF files from a directory into a single PDF saved to the specified path.

    Args:
        input_dir_path (str): Path to the directory containing PDF files to merge.
        new_name (str): The name of the merged output PDF file (without a '.pdf' extension).
        output_dir (Optional[str]): Path where the merged PDF will be saved.
            If None, defaults to input directory path.
        ask_password_callback (Optional[Callable[[str], Optional[str]]]): Function to
            get password for encrypted PDFs. Receives file path, returns password or None.

    Returns:
        Result: Object indicating success or failure, with relevant message and error type.
    """

    if not input_dir_path:
        return Result(
            success=False, title="No files", message="No input files selected."
        )

    if not new_name or new_name.strip() == "":
        return Result(
            success=False,
            title="Invalid name",
            message="Name of the merged PDF cannot be empty",
        )

    output_dir = output_dir or input_dir_path

    if not new_name.endswith(".pdf"):
        new_name += ".pdf"

    output_file_path = os.path.abspath(os.path.join(output_dir, new_name))
    pdf_files = [
        os.path.abspath(os.path.join(input_dir_path, f))
        for f in os.listdir(input_dir_path)
        if f.lower().endswith(".pdf")
    ]

    if output_file_path in pdf_files:
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
        for pdf in pdf_files:
            is_valid, status, error_message = validate_pdf_file(path=pdf)
            password: str | None = None

            # PDF is not valid AND it is corrupted or it is NOT a PDF
            if (
                not is_valid and status == PDFValidationStatus.CORRUPTED
            ) or status == PDFValidationStatus.NOT_PDF:
                invalid_files.append(pdf)
                continue

            # PDF is encrypted
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
                    skipped_encrypted_files.append(pdf)
                    continue

                # Password not provided, append in skipped_encrypted_files and continue
                if not password:
                    skipped_encrypted_files.append(pdf)
                    continue

            reader = PdfReader(pdf)
            if reader.is_encrypted:
                if password is not None:
                    decrypt_result: int = reader.decrypt(password=password)
                    if decrypt_result == 0:
                        wrong_password_files.append(pdf)
                        continue
                else:
                    skipped_encrypted_files.append(pdf)
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
        return handle_exception(exc=e, context="Merging PDFs of a directory")

    finally:
        merger.close()
