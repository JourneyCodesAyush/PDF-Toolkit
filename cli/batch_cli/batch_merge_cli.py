import argparse

from core.batch.batch_merge import batch_merge_pdfs
from core.result import Result


def add_batch_merge_arguments(parser: argparse.ArgumentParser) -> None:
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
    result: Result = batch_merge_pdfs(
        input_dir_path=args.directory,
        new_name=args.newname,
        output_dir=args.outputdirectory,
    )

    if result.success:
        print(f"{result.message}")
    else:
        print(f"{result.message}")
