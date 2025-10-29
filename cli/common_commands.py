# cli/common_commands.py

from pathlib import Path

from core import globals

SKIP_TOKEN = "__skip__"


def ask_password_cli(file: str) -> str | None:
    """
    Prompt the user to enter a password for an encrypted PDF file via CLI.

    This function is used in CLI operations to request a password for a given
    PDF file. Users can enter the password, or type a special token to skip
    the file. If the user chooses to skip, a confirmation prompt is displayed.
    Additionally, if the global setting ENCRYPTED_FILE_HANDLING is set to
    skip all encrypted files, this function will automatically return None
    without prompting.

    Args:
        file (str): The path to the encrypted PDF file for which a password is requested.

    Returns:
        str | None: The password entered by the user, or None if the file should be skipped.
                    Skipping occurs either by typing the skip token and confirming, or
                    if global settings indicate all encrypted files should be skipped.
    """

    file_name = Path(file).name
    if globals.ENCRYPTED_FILE_HANDLING == globals.EncryptedFileHandling.SKIP_ALL:
        return None

    password: str | None = input(
        f"Enter the password for {file_name} (or type {SKIP_TOKEN} to skip):"
    ).strip()

    if password.lower() == SKIP_TOKEN:
        sure: str = input(f"Are you sure you want to skip {file}? [y/N]:").strip()
        if sure == "y" or sure == "Y":
            return None

    return password
