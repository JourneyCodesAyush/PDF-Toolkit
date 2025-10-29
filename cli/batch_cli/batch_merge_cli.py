# Batch Merge CLI

import argparse

from cli.common_commands import ask_password_cli
from core.batch.batch_merge import batch_merge_pdfs
from core.result import Result


def add_batch_merge_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add command-line arguments for batch merging PDF files in a directory.

    This function registers arguments for specifying the input directory
    containing the PDFs to merge, the name for the merged output file,
    and an optional output directory to save the merged PDF.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which batch merge arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-d", "--directory", required=True, help="Directory containing PDFs to merge"
    )
    parser.add_argument(
        "-n", "--newname", required=True, help="Name of the merged PDF file"
    )
    parser.add_argument(
        "-o",
        "--outputdirectory",
        required=False,
        help="Directory to save the merged PDF",
    )


def run_batch_merge(args: argparse.Namespace) -> None:
    """
    Execute the batch merge operation using provided command-line arguments.

    This function merges all PDFs found in the specified input directory into a
    single PDF with the given name. The merged file is saved to the provided
    output directory, or to the input directory if no output is specified.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - directory (str): Path to the directory containing PDFs to merge.
            - newname (str): Name for the resulting merged PDF file.
            - outputdirectory (str, optional): Directory to save the merged PDF.

    Returns:
        None
    """

    result: Result = batch_merge_pdfs(
        input_dir_path=args.directory,
        new_name=args.newname,
        output_dir=args.outputdirectory,
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
