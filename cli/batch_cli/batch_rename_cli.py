# Batch Rename CLI

import argparse

from core.batch.batch_rename import batch_rename_pdfs
from core.result import Result


def add_batch_rename_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add command-line arguments for batch renaming PDF files in a directory.

    This function registers arguments for specifying the input directory containing
    the PDFs to rename, the base name for renaming, and an optional output directory
    to save the renamed files.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which batch rename arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-d",
        "--directory",
        required=True,
        help="Path to the directory containing PDF files to rename. Example: -d ./pdfs",
    )
    parser.add_argument(
        "-n",
        "--newname",
        required=True,
        help=(
            "Base name to use for renaming files. PDFs will be renamed sequentially "
            "using this base name (e.g., 'Invoice' → Invoice_1.pdf, Invoice_2.pdf, ...)."
        ),
    )
    parser.add_argument(
        "-o",
        "--outputdirectory",
        required=False,
        help=(
            "Directory to save the renamed PDF files. "
            "If not provided, renamed files are saved in the input directory."
        ),
    )


def run_batch_rename(args: argparse.Namespace) -> None:
    """
    Execute the batch rename operation using provided command-line arguments.

    This function renames all PDFs in the specified input directory using the given
    base name, optionally saving the renamed files to a different output directory.
    If no output directory is provided, files are saved in the input directory.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - directory (str): Path to the directory containing PDFs to rename.
            - newname (str): Base name to use when renaming files.
            - outputdirectory (str, optional): Directory to save the renamed PDFs.

    Returns:
        None
    """

    output_directory = args.outputdirectory or args.directory
    result: Result = batch_rename_pdfs(
        input_dir=args.directory,
        base_name=args.newname,
        output_dir=output_directory,
    )
    if result.success:
        print(f"{result.message}")

    else:
        print(f"Rename failed: {result.message}")