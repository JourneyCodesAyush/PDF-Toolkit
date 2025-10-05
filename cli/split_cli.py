# Split CLI

import argparse

from core.pdf_splitter import split_pdf
from core.result import Result


def add_split_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add command-line arguments for splitting pages from a PDF file.

    This function registers arguments for specifying the source PDF file,
    the page range to extract, and the output directory where the new PDF
    will be saved.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which split arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        type=str,
        help="Path to the source PDF file. Example: -f document.pdf",
    )
    parser.add_argument(
        "-r",
        "--range",
        required=True,
        type=str,
        help=(
            "Page range(s) to extract. Examples:\n"
            "  '1'        → extracts page 1\n"
            "  '2-4'      → extracts pages 2 through 4\n"
            "  '1,3,5-7'  → extracts pages 1, 3, and 5 through 7"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        help="Directory where the extracted PDF(s) will be saved. Example: -o ./output",
    )


def run_split(args: argparse.Namespace) -> None:
    """
    Execute the PDF split operation using the provided command-line arguments.

    This function calls the split logic with the specified file, page range,
    and output directory. It prints the result to the console indicating
    whether the operation was successful or failed.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - file (str): Path to the source PDF file.
            - range (str): Page range to extract (e.g., '1', '2-4', '1,3,5-7').
            - output (str): Directory to save the resulting split PDF.

    Returns:
        None
    """

    result: Result = split_pdf(
        file_path=args.file,
        page_range_input=args.range,
        output_dir=args.output,
    )
    if result.success:
        print(f"Pages extracted from {args.file} and saved to {args.output}")
    else:
        print(f"{result.message}")


