# Rename CLI

import argparse
from pathlib import Path

from core.pdf_rename import rename_pdf_file
from core.result import Result


def add_rename_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add command-line arguments for renaming a PDF file to the argument parser.

    This function registers the necessary arguments for the PDF rename operation,
    including the path to the original PDF and the desired new name or path.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which rename arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the existing PDF file you want to rename. Example: -f old.pdf",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help=(
            "New name or path for the renamed PDF. "
            "You can provide just a filename (e.g., new.pdf) or a full path "
            "(e.g., ./renamed/new.pdf)."
        ),
    )


def run_rename(args: argparse.Namespace) -> None:
    """
    Execute the PDF rename operation using provided command-line arguments.

    This function extracts the new file name and directory from the output path,
    then invokes the rename logic. It prints the result to the console to indicate
    success or failure.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - file (str): Path to the existing PDF file.
            - output (str): New full path or name for the renamed PDF.

    Returns:
        None
    """

    new_name = Path(args.output).name
    new_directory = str(Path(args.output).parent)

    result: Result = rename_pdf_file(
        old_path=args.file, new_directory=new_directory, new_name=new_name
    )
    if result.success:
        print(f"Renamed {args.file} to {args.output}")
    else:
        print(f"Rename failed: {result.message}")


