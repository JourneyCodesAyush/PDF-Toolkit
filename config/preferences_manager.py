# User Preferences

"""
Manages persistent user preferences stored in a JSON file within user configuration directory.
"""

import json
from pathlib import Path

from core.utils import get_persistent_path

PREFER_DIR = Path(get_persistent_path("user_config"))

PREFER_DIR.mkdir(parents=True, exist_ok=True)

USER_PREFERENCES = PREFER_DIR / "preferences.json"

DEFAULT_PREFERENCES = {
    "save_preferences": False,
    "last_merged_input_file": None,
    "last_renamed_file": None,
    "last_split_file": None,
    "last_extract_file": None,
    "batch_last_merged_folder": None,
    "batch_last_renamed_folder": None,
    "batch_last_split_file": None,
}


def get_preferences() -> dict[str, bool | str | None]:
    """
    Retrieve user preferences from the JSON file.

    If the preferences file does not exist or is invalid, it is created with default values.
    Ensures that all required keys are present in the returned dictionary, filling in
    missing keys with defaults.

    Returns:
        dict[str, bool | str | None]: A dictionary containing the user preferences:
            save_preferences (bool)
            last_merged_input_file (str | None)
            last_renamed_file (str | None)
            last_split_file (str | None)
            last_extract_file (str | None)
            batch_last_merged_folder (str | None)
            batch_last_renamed_folder (str | None)
            batch_last_split_file (str | None)
    """

    if not USER_PREFERENCES.exists():
        # set_preferences()
        with open(USER_PREFERENCES, mode="w", encoding="utf-8") as f:
            json.dump(DEFAULT_PREFERENCES, f, indent=4)
        return DEFAULT_PREFERENCES

    try:
        with open(USER_PREFERENCES, mode="r", encoding="utf-8") as f:
            user_data = json.load(f)

    except (json.JSONDecodeError, OSError):
        # set_preferences()
        with open(USER_PREFERENCES, mode="w", encoding="utf-8") as f:
            json.dump(DEFAULT_PREFERENCES, f, indent=4)

        return DEFAULT_PREFERENCES

    for key, default_value in DEFAULT_PREFERENCES.items():
        user_data.setdefault(key, default_value)

    return user_data


def set_preferences(
    last_merged_input_file: str | None = None,
    last_renamed_file: str | None = None,
    last_split_file: str | None = None,
    last_extract_file: str | None = None,
    batch_last_merged_folder: str | None = None,
    batch_last_renamed_folder: str | None = None,
    batch_last_split_file: str | None = None,
) -> None:
    """
    Update and save user preferences to the JSON file.

    Only the preferences passed as arguments are updated; others remain unchanged.

    Args:
        last_merged_input_file (str | None) : Path (string) of the last merged PDF file, or None to leave unchanged.
        last_renamed_file (str | None) : Path (string) of the last renamed PDF file, or None to leave unchanged.
        last_split_file (str | None) : Path (string) of the last split PDF file, or None to leave unchanged.
        last_extract_file (str | None) : Path (string) of the last extracted PDF file, or None to leave unchanged.
        batch_last_merged_folder (str | None) : Path (string) of the last folder used for batch merging, or None to leave unchanged.
        batch_last_renamed_folder (str | None) : Path (string) of the last folder used for batch renaming, or None to leave unchanged.
        batch_last_split_file (str | None) : Path (string) of the last file used for batch splitting, or None to leave unchanged.

    Returns:
        None
    """

    prefs = get_preferences()

    if last_merged_input_file is not None:
        prefs["last_merged_input_file"] = last_merged_input_file

    if last_renamed_file is not None:
        prefs["last_renamed_file"] = last_renamed_file

    if last_split_file is not None:
        prefs["last_split_file"] = last_split_file

    if last_extract_file is not None:
        prefs["last_extract_file"] = last_extract_file

    if batch_last_merged_folder is not None:
        prefs["batch_last_merged_folder"] = batch_last_merged_folder

    if batch_last_renamed_folder is not None:
        prefs["batch_last_renamed_folder"] = batch_last_renamed_folder

    if batch_last_split_file is not None:
        prefs["batch_last_split_file"] = batch_last_split_file

    with open(USER_PREFERENCES, mode="w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=4)
