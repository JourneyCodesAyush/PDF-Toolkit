# Nothing much

import argparse

from core.pdf_merge import merge_pdf
from core.result import Result


def add_merge_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-f", "--files", nargs="+", required=True, help="List of PDFs to merge"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Location to save the merged PDF"
    )


def run_merge(args: argparse.Namespace) -> None:
    result: Result = merge_pdf(input_file_path=args.files, output_file_path=args.output)
    if result.success:
        print(f"{args.files} merged and saved to {args.output}")
    else:
        print(f"{result.message}")
