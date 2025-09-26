import argparse

from pathlib import Path
from core.result import Result
from core.batch.batch_split import batch_split_pdf


def add_batch_split_arguments(parser: argparse.ArgumentParser):
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
    output_directory = args.outputdirectory or str(Path(args.file).parent)
    result: Result = batch_split_pdf(file_path=args.file, output_dir=output_directory)
    if result.success:
        print(f"{result.message}")

    else:
        print(f"Split failed: {result.message}")
