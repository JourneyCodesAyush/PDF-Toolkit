# Shared utilities

def parse_page_ranges(page_range_input: str, total_pages: int) -> tuple[list[tuple[int, int]] | None, str | None]:
    """
    Parses a page range input string like "1-3,5,7-9".

    Args:
        page_range_input (str): User input string.
        total_pages (int): Total number of pages in the PDF.

    Returns:
        (ranges, error): 
            - ranges: List of (start, end) tuples if successful, else None
            - error: Error message string if failed, else None
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
                    return None, f"Start page {start} cannot be greater than end page {end}"
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
