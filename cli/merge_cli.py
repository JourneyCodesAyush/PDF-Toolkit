# Merge CLI

import argparse

from cli.common_commands import ask_password_cli
from core.pdf_merge import merge_pdf
from core.result import Result


def add_merge_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add command-line arguments for merging PDF files to the argument parser.

    This function registers the necessary arguments for the PDF merge operation,
    including the list of input PDF files and the output file path.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which merge arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-f", "--files", nargs="+", required=True, help="List of PDFs to merge"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Location to save the merged PDF"
    )


def run_merge(args: argparse.Namespace) -> None:
    """
    Execute the PDF merge operation using provided command-line arguments.

    This function calls the merge logic with the given input and output paths.
    It prints the result to the console, indicating success or failure.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - files (list[str]): List of PDF file paths to merge.
            - output (str): Output path for the merged PDF.

    Returns:
        None
    """

    result: Result = merge_pdf(
        input_file_path=args.files,
        output_file_path=args.output,
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
