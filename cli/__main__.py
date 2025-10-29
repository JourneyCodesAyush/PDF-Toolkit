# All the functions for CLI

import argparse

from cli.batch_cli.batch_merge_cli import add_batch_merge_arguments, run_batch_merge
from cli.batch_cli.batch_rename_cli import add_batch_rename_arguments, run_batch_rename
from cli.batch_cli.batch_split_cli import add_batch_split_arguments, run_batch_split
from cli.merge_cli import add_merge_arguments, run_merge
from cli.rename_cli import add_rename_arguments, run_rename
from cli.split_cli import add_split_arguments, run_split
from core.globals import EncryptedFileHandling
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

    parser = argparse.ArgumentParser(description="CLI version of the PDF-Toolkit")

    sub_parser = parser.add_subparsers(
        title="Sub commands for operations", dest="subcommand"
    )

    merge_subparser = sub_parser.add_parser("merge", help="Merge multiple pdfs")
    add_merge_arguments(merge_subparser)
    merge_subparser.set_defaults(func=run_merge)

    rename_subparser = sub_parser.add_parser("rename", help="Rename pdf")
    add_rename_arguments(rename_subparser)
    rename_subparser.set_defaults(func=run_rename)

    split_subparser = sub_parser.add_parser("split", help="Split pdf")
    add_split_arguments(split_subparser)
    split_subparser.set_defaults(func=run_split)

    batch_split_subparser = sub_parser.add_parser(
        "batch_split", help="Split PDF into single page PDFs"
    )
    add_batch_split_arguments(batch_split_subparser)
    batch_split_subparser.set_defaults(func=run_batch_split)

    batch_merge_subparser = sub_parser.add_parser(
        "batch_merge", help="Merge pdfs in a directory to a single PDF"
    )
    add_batch_merge_arguments(batch_merge_subparser)
    batch_merge_subparser.set_defaults(func=run_batch_merge)

    batch_rename_subparser = sub_parser.add_parser(
        "batch_rename", help="Rename PDFs of a directory"
    )
    add_batch_rename_arguments(batch_rename_subparser)
    batch_rename_subparser.set_defaults(func=run_batch_rename)

    parser.add_argument(
        "-v", "--version", action="store_true", help="Show the version of the tool"
    )

    parser.add_argument(
        "--skip-all",
        action="store_const",
        const=EncryptedFileHandling.SKIP_ALL,
        dest="enc_mode",
        help="Skip all encrypted PDFs",
    )

    args = parser.parse_args()
    if args.enc_mode:
        import core.globals

        core.globals.ENCRYPTED_FILE_HANDLING = EncryptedFileHandling.SKIP_ALL

    if args.version:
        print(f"PDF-Toolkit v{__version__}")
    elif hasattr(args, "func"):
        args.func(args)
    else:
        print(
            "No subcommand provided. Try 'merge', 'split', 'rename', or a batch command."
        )
        parser.print_help()


if __name__ == "__main__":
    main()
