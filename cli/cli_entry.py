# All the functions for CLI

import argparse

from cli.batch_cli.batch_merge_cli import (add_batch_merge_arguments,
                                           run_batch_merge)
from cli.batch_cli.batch_rename_cli import (add_batch_rename_arguments,
                                            run_batch_rename)
from cli.batch_cli.batch_split_cli import (add_batch_split_arguments,
                                           run_batch_split)
from cli.merge_cli import add_merge_arguments, run_merge
from cli.rename_cli import add_rename_arguments, run_rename
from cli.split_cli import add_split_arguments, run_split
from version import __version__


def main() -> None:
    """
    Entry point for the PDF-Toolkit CLI.

    This function parses top-level command-line arguments and dispatches
    control to the appropriate sub-command handler (e.g., merge, split, rename,
    batch operations). It supports mutually exclusive actions including:

        - Merge PDFs
        - Rename a single PDF
        - Split or extract pages from a PDF
        - Batch merge PDFs from a directory
        - Batch rename PDFs in a directory
        - Batch split a PDF into individual pages
        - Show the current version

    For each action, it delegates parsing of action-specific arguments and
    execution to the respective CLI modules.

    Returns:
        None
    """

    parser = argparse.ArgumentParser(
        prog="pdf-toolkit",
        description=(
            "PDF-Toolkit: A command-line tool for managing PDF files.\n\n"
            "Available operations include:\n"
            "  - Merge PDFs into one file\n"
            "  - Split or extract pages\n"
            "  - Rename a single PDF\n"
            "  - Perform batch operations (merge, split, rename) on directories"
        ),
        epilog=(
            "Examples:\n"
            "  pdf-toolkit --merge --input file1.pdf file2.pdf --output merged.pdf\n"
            "  pdf-toolkit --split --input document.pdf --pages 1-3 --output part.pdf\n"
            "  pdf-toolkit --rename --input old.pdf --output new.pdf\n"
            "  pdf-toolkit --batch-merge --input-dir ./pdfs --output merged.pdf\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    action_group = parser.add_mutually_exclusive_group(required=True)

    action_group.add_argument(
        "--merge",
        action="store_true",
        help="Merge multiple PDF files into a single PDF (requires --input and --output)",
    )

    action_group.add_argument(
        "--rename",
        action="store_true",
        help="Rename a PDF file (requires --input and --output)",
    )
    action_group.add_argument(
        "--split",
        action="store_true",
        help="Split a PDF into multiple files or extract specific pages (requires --input, --pages, and --output)",
    )
    action_group.add_argument(
        "--batch-merge",
        action="store_true",
        help="Batch merge PDFs from a directory (requires --input-dir and --output)",
    )
    action_group.add_argument(
        "--batch-rename",
        action="store_true",
        help="Batch rename PDFs in a directory (requires --input-dir and --pattern)",
    )
    action_group.add_argument(
        "--batch-split",
        action="store_true",
        help="Batch split PDFs into individual pages (requires --input-dir and --output-dir)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"PDF-Toolkit v{__version__}",
        help="Show the current version of PDF-Toolkit and exit",
    )

    args, remaining_args = parser.parse_known_args()

    if args.version:
        print(f"v{__version__}")
    elif args.rename:
        op_parser = argparse.ArgumentParser(
            prog="pdf-toolkit --rename",
            description="Rename a single PDF file by providing an input file and a new output name.",
            epilog="Example:\n  pdf-toolkit --rename --input old.pdf --output new.pdf",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        add_rename_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_rename(op_args)
    elif args.merge:
        op_parser = argparse.ArgumentParser(
            prog="pdf-toolkit --merge",
            description="Merge multiple PDF files into a single PDF document.",
            epilog="Example:\n  pdf-toolkit --merge --input file1.pdf file2.pdf --output merged.pdf",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        add_merge_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_merge(op_args)
    elif args.split:
        op_parser = argparse.ArgumentParser(
            prog="pdf-toolkit --split",
            description="Split a PDF into multiple files or extract specific pages.",
            epilog=(
                "Examples:\n"
                "  pdf-toolkit --split --input document.pdf --pages 1-3 --output part.pdf\n"
                "  pdf-toolkit --split --input book.pdf --pages 5 --output single_page.pdf"
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        add_split_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_split(op_args)
    elif args.batch_rename:
        op_parser = argparse.ArgumentParser(
            prog="pdf-toolkit --batch-rename",
            description="Rename multiple PDF files in a directory using a naming pattern.",
            epilog=(
                "Example:\n"
                "  pdf-toolkit --batch-rename --input-dir ./pdfs --pattern 'document_{n}.pdf'\n"
                "This will rename all PDFs in ./pdfs to document_1.pdf, document_2.pdf, etc."
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        add_batch_rename_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_batch_rename(op_args)
    elif args.batch_merge:
        op_parser = argparse.ArgumentParser(
            prog="pdf-toolkit --batch-merge",
            description="Merge all PDF files in a directory into a single PDF document.",
            epilog="Example:\n  pdf-toolkit --batch-merge --input-dir ./pdfs --output merged.pdf",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        add_batch_merge_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_batch_merge(op_args)
    elif args.batch_split:
        op_parser = argparse.ArgumentParser(
            prog="pdf-toolkit --batch-split",
            description="Split all PDFs in a directory into individual single-page PDF files.",
            epilog="Example:\n  pdf-toolkit --batch-split --input-dir ./pdfs --output-dir ./output",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        add_batch_split_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_batch_split(op_args)


if __name__ == "__main__":
    main()
