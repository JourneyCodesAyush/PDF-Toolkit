# Split CLI

import argparse

from cli.common_commands import ask_password_cli
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
        "-f", "--file", required=True, help="PDF to extract pages from", type=str
    )
    parser.add_argument(
        "-r",
        "--range",
        required=True,
        help="Page to extract (e.g., '1', '2-4', or '1,3,5-7')",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Directory to save the split PDF",
        type=str,
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
        ask_password_callback=ask_password_cli,
    )
    if result.success:
        print(result.message)
        data = result.data or {}
        if data.get("skipped_encrypted_files"):
            print("Skipped encrypted PDFs:", ", ".join(data["skipped_encrypted_files"]))
        if data.get("wrong_password_files"):
            print("PDFs with wrong passwords:", ", ".join(data["wrong_password_files"]))
        if data.get("invalid_files"):
            print("Invalid PDFs:", ", ".join(data["invalid_files"]))

    else:
        print(f"{result.message}")
