# Nothing much

import argparse
from pathlib import Path

from core.pdf_rename import rename_pdf_file
from core.result import Result


def add_rename_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-f", "--file", required=True, help="PDF to rename")
    parser.add_argument("-o", "--output", required=True, help="New name of the PDF")


def run_rename(args: argparse.Namespace) -> None:
    new_name = Path(args.output).name
    new_directory = str(Path(args.output).parent)

    result: Result = rename_pdf_file(
        old_path=args.file, new_directory=new_directory, new_name=new_name
    )
    if result.success:
        print(f"Renamed {args.file} to {args.output}")
    else:
        print(f"Rename failed: {result.message}")
