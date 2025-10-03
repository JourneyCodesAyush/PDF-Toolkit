# Merge CLI

import argparse

from core.pdf_merge import merge_pdf
from core.result import Result


def add_merge_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add command-line arguments for merging PDF files to the argument parser.

    This function registers the necessary arguments for the PDF merge operation,
    including the list of input PDF files and the output file path.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which merge arguments are added.

    Returns:
        None
    """

    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        required=True,
        help=(
            "One or more PDF files to merge, provided in the desired order. "
            "Example: -f file1.pdf file2.pdf file3.pdf"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path to save the merged PDF file. Example: -o merged.pdf",
    )


def run_merge(args: argparse.Namespace) -> None:
    """
    Execute the PDF merge operation using provided command-line arguments.

    This function calls the merge logic with the given input and output paths.
    It prints the result to the console, indicating success or failure.

    Args:
        args (argparse.Namespace): Parsed command-line arguments containing:
            - files (list[str]): List of PDF file paths to merge.
            - output (str): Output path for the merged PDF.

    Returns:
        None
    """

    result: Result = merge_pdf(input_file_path=args.files, output_file_path=args.output)
    if result.success:
        print(f"{args.files} merged and saved to {args.output}")
    else:
        print(f"{result.message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pdf-toolkit merge",
        description="Merge multiple PDF files into a single PDF document.",
        epilog=(
            "Example:\n"
            "  pdf-toolkit --merge -f file1.pdf file2.pdf --output merged.pdf"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_merge_arguments(parser)
    args = parser.parse_args()
    run_merge(args)
