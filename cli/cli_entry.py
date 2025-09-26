# All the functions for CLI

import argparse

from cli.batch_cli.batch_merge_cli import add_batch_merge_arguments, run_batch_merge
from cli.batch_cli.batch_rename_cli import add_batch_rename_arguments, run_batch_rename
from cli.batch_cli.batch_split_cli import add_batch_split_arguments, run_batch_split
from cli.merge_cli import add_merge_arguments, run_merge
from cli.rename_cli import add_rename_arguments, run_rename
from cli.split_cli import add_split_arguments, run_split
from version import __version__


def main():
    parser = argparse.ArgumentParser(description="CLI version of the PDF-Toolkit")

    action_group = parser.add_mutually_exclusive_group(required=True)

    action_group.add_argument("--merge", action="store_true", help="Merge PDF files")
    action_group.add_argument("--rename", action="store_true", help="Rename a PDF file")
    action_group.add_argument(
        "--split", action="store_true", help="Split/extract pages from PDF"
    )
    action_group.add_argument(
        "--batch-merge", action="store_true", help="Batch merge PDF files"
    )
    action_group.add_argument(
        "--batch-rename", action="store_true", help="Batch rename a PDF file"
    )
    action_group.add_argument(
        "--batch-split", action="store_true", help="Batch split pages from PDF"
    )
    action_group.add_argument(
        "-v", "--version", action="store_true", help="Current version of the project"
    )

    args, remaining_args = parser.parse_known_args()

    if args.version:
        print(f"v{__version__}")
    elif args.rename:
        op_parser = argparse.ArgumentParser(description="Rename PDF")
        add_rename_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_rename(op_args)
    elif args.merge:
        op_parser = argparse.ArgumentParser(description="Merge PDFs")
        add_merge_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_merge(op_args)
    elif args.split:
        op_parser = argparse.ArgumentParser(
            description="Split or Extract page from PDF"
        )
        add_split_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_split(op_args)
    elif args.batch_rename:
        op_parser = argparse.ArgumentParser(description="Batch rename PDFs")
        add_batch_rename_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_batch_rename(op_args)
    elif args.batch_merge:
        op_parser = argparse.ArgumentParser(description="Batch merge PDFs")
        add_batch_merge_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_batch_merge(op_args)
    elif args.batch_split:
        op_parser = argparse.ArgumentParser(description="Batch split PDFs")
        add_batch_split_arguments(op_parser)
        op_args = op_parser.parse_args(remaining_args)
        run_batch_split(op_args)


if __name__ == "__main__":
    main()
