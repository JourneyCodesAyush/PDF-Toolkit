# Batch Split CLI

import argparse

from pathlib import Path
from core.result import Result
from core.batch.batch_split import batch_split_pdf


def add_batch_split_arguments(parser: argparse.ArgumentParser):
    """
    Add command-line arguments for batch splitting a PDF into individual pages.

    This function registers arguments for specifying the source PDF file
    and the optional output directory where the individual page PDFs
    will be saved.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which batch split arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-f", "--file", required=True, help="PDF file to split into individual pages"
    )
    parser.add_argument(
        "-o",
        "--outputdirectory",
        required=False,
        help="Directory to save the split PDFs",
    )


def run_batch_split(args: argparse.Namespace):
    """
    Execute the batch split operation using provided command-line arguments.

    This function splits the input PDF into separate pages and saves each page
    as an individual PDF in the specified output directory. If no output directory
    is provided, the files are saved in the same directory as the input file.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - file (str): Path to the source PDF file.
            - outputdirectory (str, optional): Directory to save the individual page PDFs.

    Returns:
        None
    """

    output_directory = args.outputdirectory or str(Path(args.file).parent)
    result: Result = batch_split_pdf(file_path=args.file, output_dir=output_directory)
    if result.success:
        print(f"{result.message}")

    else:
        print(f"Split failed: {result.message}")
