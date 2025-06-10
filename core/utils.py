# Shared utilities

import os
import sys


def get_absolute_path(relative_path: str = "") -> str:
    """
    Get the absolute path to a bundled resource, such as an icon or asset file.

    This function returns a path that works both during development
    and when the app is bundled by PyInstaller. When running as a bundled
    executable, it returns the path inside PyInstaller’s temporary unpack folder
    (sys._MEIPASS), where read-only resources are extracted.

    Args:
    relative_path (str): Relative path from the root of the project or executable file

    Returns:
    str: Absolute path
    """

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
        # base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        # base_path = os.path.abspath(".")

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
        base_path = os.path.dirname(os.path.abspath(__file__))
        # base_path = os.path.abspath(".")
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
