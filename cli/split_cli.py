# Nothing much

import argparse
from pathlib import Path

from core.pdf_splitter import split_pdf
from core.result import Result


def add_split_arguments(parser: argparse.ArgumentParser) -> None:
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
    result: Result = split_pdf(
        file_path=args.file,
        page_range_input=args.range,
        output_dir=str(Path(args.output).parent),
    )
    if result.success:
        print(f"Pages extracted from {args.file} and saved to {args.output}")
    else:
        print(f"{result.message}")
