# Shared utilities

import os
import platform
import sys
from enum import Enum
from pathlib import Path

from PyPDF2 import PdfReader


def _get_windows_data():
    """
    Returns the base directory for user-local application data on Windows.

    Uses the LOCALAPPDATA environment variable.

    Raises:
        ValueError: If LOCALAPPDATA is not set.
    """
    value = os.getenv("LOCALAPPDATA")
    if not value:
        raise ValueError("LOCALAPPDATA is not set")
    return Path(value)


def _get_macos_data():
    """
    Returns the base directory for user-local application data on macOS.

    Typically: ~/Library/Application Support
    """
    return Path.home() / "Library" / "Application Support"


def _get_linux_data():
    """
    Returns the base directory for user-local application data on Linux/BSD.

    Uses $XDG_DATA_HOME if set, otherwise falls back to ~/.local/share
    """
    xdg = os.getenv("XDG_DATA_HOME")
    if xdg:
        return Path(xdg)
    else:
        return Path.home() / ".local" / "share"


def get_app_data_dir() -> Path:
    """
    Returns the PDF Toolkit root directory for storing user data.

    Cross-platform paths:
    - Windows: %LOCALAPPDATA%\\.pdf-toolkit
    - macOS: ~/Library/Application Support/.pdf-toolkit
    - Linux/BSD: $XDG_DATA_HOME/pdf-toolkit or ~/.local/share/pdf-toolkit

    Returns:
        Path: Path to PDF Toolkit app data directory
    """
    if platform.system() == "Windows":
        PDF_TOOLKIT_DIR = _get_windows_data() / ".pdf-toolkit"
    elif platform.system() == "Darwin":
        PDF_TOOLKIT_DIR = _get_macos_data() / ".pdf-toolkit"
    else:
        PDF_TOOLKIT_DIR = _get_linux_data() / ".pdf-toolkit"

    return PDF_TOOLKIT_DIR


def get_absolute_path(relative_path: str = "") -> str:
    """
    Get the absolute path to a bundled resource, such as an icon or asset file.

    This function returns a path that works both during development
    and when the app is bundled by PyInstaller. When running as a bundled
    executable, it returns the path inside PyInstaller's temporary unpack folder
    (sys._MEIPASS), where read-only resources are extracted.

    Args:
    relative_path (str): Relative path from the root of the project or executable file

    Returns:
    str: Absolute path
    """

    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        # base_path = sys._MEIPASS
        # base_path = os.path.dirname(sys.executable)
    else:
        # base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_persistent_path(relative_path: str = "") -> str:
    """
    Get the absolute path to a writable file or folder location next to the executable.

    This function returns a persistent path suitable for saving logs, configuration,
    or user data. When running as a bundled executable, the path is relative to the
    directory containing the executable itself, ensuring data persists after exit.
    During development, it defaults to the current working directory.

    Args:
        relative_path (str): Relative path from the root of the project or executable file.

    Returns:
        str: Absolute path.
    """
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)  # persistent folder next to exe
    else:
        # base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def parse_page_ranges(
    page_range_input: str, total_pages: int
) -> tuple[list[tuple[int, int]] | None, str | None]:
    """
    Parse a string representing page ranges into a list of (start, end) tuples.

    Args:
        page_range_input (str): Page range string (e.g., "1-3,5,7-9").
        total_pages (int): Total pages in the PDF to validate ranges.

    Returns:
        tuple[list[tuple[int, int]] | None, str | None]:
            - List of (start, end) page tuples if parsing is successful, else None.
            - Error message string if parsing fails, else None.
    """
    page_range_strings = page_range_input.split(",")
    parsed_ranges = []

    for segment in page_range_strings:
        segment = segment.strip()
        if not segment:
            continue

        if "-" in segment:
            try:
                start, end = map(int, segment.split("-"))
                if start > end:
                    return (
                        None,
                        f"Start page {start} cannot be greater than end page {end}",
                    )
            except ValueError:
                return None, f"Invalid range format: '{segment}'"
        else:
            try:
                start = end = int(segment)
            except ValueError:
                return None, f"Invalid page number: '{segment}'"

        if start < 1 or end > total_pages:
            return None, f"Page range {start}-{end} is out of bounds (1–{total_pages})"

        parsed_ranges.append((start, end))

    if not parsed_ranges:
        return None, "No valid page ranges provided"

    return parsed_ranges, None


class PDFValidationStatus(Enum):
    """
    Enum representing the validation status of a PDF file.

    Members:
        - VALID: The PDF file is valid, readable, and unencrypted.
        - NOT_PDF: The file is not a PDF based on its extension.
        - ENCRYPTED: The PDF file is encrypted or password-protected.
        - CORRUPTED: The PDF file is corrupted or unreadable.

    Used to standardize the results of PDF validation checks across the app.
    """

    VALID = "valid"
    NOT_PDF = "not-pdf"
    ENCRYPTED = "encrypted"
    CORRUPTED = "corrupted"


def is_valid_pdf(path: str) -> bool:
    """
    Check whether a file is a readable, non-corrupted PDF.

    Attempts to load the file with PyPDF2 and access its pages to confirm validity.

    Args:
        path (str): Path to the PDF file.

    Returns:
        bool:
            - True if the file can be read as a valid PDF.
            - False if the file is corrupted or unreadable.
    """
    try:
        reader = PdfReader(path)
        _ = reader.pages
        return True
    except Exception as e:
        return False


def is_encrypted_pdf(path: str) -> bool:
    """
    Determine whether a PDF file is encrypted or password-protected.

     Args:
         path (str): Path to the PDF file.

     Returns:
         bool:
             - True if the file is encrypted.
             - False if the file is not encrypted or if the check fails.
    """
    try:
        reader = PdfReader(path)
        return reader.is_encrypted
    except Exception as e:
        return False


def validate_pdf_file(path: str) -> tuple[bool, PDFValidationStatus, str]:
    """
    Validate whether the file is a legitimate, readable, and unencrypted PDF.

    This function performs the following checks in order:
      - Ensures the file has a ".pdf" extension.
      - Confirms the file can be opened and parsed by PyPDF2.
      - Detects whether the file is encrypted or password-protected.

    Args:
        path (str): Path to the file to validate.

    Returns:
        tuple[bool, PDFValidationStatus, str]:
            - bool: True if valid PDF and neither encrypted nor corrupt, False otherwise.
            - PDFValidationStatus: Enum indicating the validation result status.
            - str: Detailed error message if validation fails; empty string if successful.
    """
    if not path.lower().endswith(".pdf"):
        return (False, PDFValidationStatus.NOT_PDF, "File is not a .pdf file.")

    if not is_valid_pdf(path):
        return (
            False,
            PDFValidationStatus.CORRUPTED,
            "The file is not a valid PDF or is corrupted",
        )

    if is_encrypted_pdf(path):
        return (
            False,
            PDFValidationStatus.ENCRYPTED,
            "The file is encrypted and cannot be processed",
        )

    return (True, PDFValidationStatus.VALID, "")
