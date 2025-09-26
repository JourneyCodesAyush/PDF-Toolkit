import argparse

from core.batch.batch_rename import batch_rename_pdfs
from core.result import Result


def add_batch_rename_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-d", "--directory", required=True, help="Directory containing PDFs to rename"
    )
    parser.add_argument(
        "-n",
        "--newname",
        required=True,
        help="Base name to use when renaming PDFs (e.g. 'Invoice' → Invoice_1.pdf, Invoice_2.pdf...)",
    )
    parser.add_argument(
        "-o",
        "--outputdirectory",
        required=False,
        help="Directory to save the renamed PDFs",
    )


def run_batch_rename(args: argparse.Namespace) -> None:
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
