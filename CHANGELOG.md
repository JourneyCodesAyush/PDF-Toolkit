# 📄 Changelog

All notable changes to this project will be documented in this file.

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) guidelines and uses [Semantic Versioning](https://semver.org/).

---

## [v1.2.0] – 2025-10-24

### ✨ Added

- 🛡️ GUI prompt for encrypted PDFs: operations now ask for password instead of stopping abruptly.
- 🔗 Core modules updated to support password callbacks for encrypted PDFs.
- ⚡ Root window is automatically maximized.

---

## [v1.1.0] – 2025-09-27

### ✨ Added

- 🚀 Added CLI support for automation geeks.
- 🎉 Celebrated 200+ commits milestone.
- 📄 Improved docstrings for better code documentation.

---

## [v1.0.0] – 2025-09-13

### 🎉 Stable Release

After several pre-release versions and months of iteration, PDF Toolkit is now officially stable and production-ready.
This version includes a complete UI overhaul, improved cross-platform compatibility, and robust internal logging.

---

### ✨ Added

- **CustomTkinter UI Overhaul**:
  - Switched from vanilla Tkinter to [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), offering a modern, native-feeling UI experience.
  - Introduced consistent theming, rounded buttons, smooth fonts, and responsive resizing.
  - Reworked navigation and layout for easier access to Merge, Rename, Split features.
- **Improved layout logic** in `main_window.py` for better scaling across screen sizes.
- **Batch Tooltips and Help Labels** added for better usability.

---

### 🛠 Refactored

- Refactored GUI files (`main_window.py`, `batch_operations_gui.py`, `common_ui.py`) to support CustomTkinter widgets and layout patterns.
- Updated asset loading to support newer image formats compatible with CTk.

---

### 🐞 Fixed

- `bugfix(gui/main-window)`: Fixed critical issue where images (icons) would not load correctly in the standalone executable by using `get_absolute_path()` for asset resolution.

---

## [v0.9.0] – 2025-08-28

### ✨ Added

- **Persistent User Preferences**:
  - Support for saving recent file paths and user actions in `user_config/preferences.json`.
  - Preferences such as last used files and folders for merge, rename, and split operations are now remembered across sessions.

### 🐞 Fixed

- Resolved `RecursionError` caused by missing `preferences.json` on first-time use.
- Improved error logging and handling for corrupted or missing preferences files.

### 🧱 Improved

- Correct handling of `user_config` and `logs` directories in both source and PyInstaller builds.
- Enhanced path resolution using `get_persistent_path()`, improving cross-platform compatibility and stability.

---

## [v0.8.0] – 2025-08-23

### ✨ Added

- Migrated serious error logging from `logs/error.log` to `logs/error.ndjson` using structured JSON lines format, improving both machine parsing and human readability while maintaining existing error capture and user-friendly messaging.

### 🐞 Fixed

- `core/utils.py`: Use `getattr()` to safely access `_MEIPASS` in `get_absolute_path()` — prevents errors during PyInstaller execution

---

## [v0.7.0] – 2025-08-15

### ✨ Added

- New **Extract** module to extract custom page ranges from PDFs (e.g., `5-7`)
- Unit tests covering the Extract module to ensure correctness and robustness
- Updated GUI to include Extract functionality with user-friendly page range input

### 🧪 Testing

- Added tests specifically for Extract module in `tests/core_test/test_pdf_extract.py`

---

## [v0.6.0] – 2025-07-27

### ✨ Added

- `tests/` directory with unit tests for all core operations:
  - `tests/conftest.py`: Contains shared fixtures for all tests
  - `tests/core_test/`: Includes test files corresponding to modules in `core/`
  - `tests/core_test/batch_test/`: Includes test files for modules in `core/batch/`
- 🧪 Initial test suite covering:
  - Core modules: merge, split, rename
  - Batch modules: batch-merge, batch-split, batch-rename

---

## [v0.5.0] – 2025-07-26

### 🛡️ Improved

- Added stricter validation in **batch rename** to prevent input errors and handle the output location where the files would be saved

### 🐞 Fixed

- **core/rename**: Add validation for empty file name
- **core/merge**: Prevent overwriting an existing file, add output path validations, and avoid self-merge scenarios
- **core/batch-merge**: Ensure the new name is not empty and the output file does not already exist
- **core/batch-split**: Assign the output directory to a variable before checking its validity to prevent runtime errors

---

## [v0.4.1] – 2025-07-05

### 🐞 Fixed

- Replace `.ico` icon with `.png` to improve compatibility with Linux desktop environments

---

## [v0.4.0] – 2025-07-03

### ✨ Added

- **Progress bar and threading support for long-running operations**:
  - Introduced a reusable `ProgressBar` modal window in `gui/common_ui.py`
  - New `run_task_with_progress()` function allows running any `Result`-returning task in a background thread
  - Keeps GUI responsive during operations like merge, split, rename (batch and single)
  - Safe GUI lock using `grab_set()` and `WM_DELETE_WINDOW` override

### 🔧 Changed

- All long-running operations now execute in background threads
- Main UI remains interactive during PDF processing tasks
- Enhanced error resilience and encapsulation of shared UI behaviors

### 🐞 Fixed

- Fixed UI freeze when performing large PDF operations in batch mode
- Minor alignment and modality bugs in batch dialogs

---

## [v0.3.0] – 2025-06-27

### ✨ Added

- Batch processing support for PDFs:
  - Batch merge, rename, and split operations implemented in `core/batch/` and `gui/batch/`
  - New GUI dialogs for selecting folders or multiple PDFs for batch actions
  - Comprehensive logging of batch operations in `user_activity.log`
- Enhanced error handling and user messaging consistency across batch features

---

## [v0.2.1] – 2025-06-18

### ✨ Added

- Separate logging for **user-facing messages** and **developer-focused error logs**
- Improved error handling with clearer separation between user feedback and internal logging
- Refactored GUI error reporting:
  - Streamlined usage of `show_message()` and `handle_exception()`
  - More consistent logging of `Result.success` outcomes

---

## [v0.2.0] – 2025-06-13

### ✨ Added

- **Advanced PDF validation** before merge, split, and rename operations:
  - Verifies `.pdf` extension
  - Detects corrupted or unreadable files
  - Detects encrypted (password-protected) PDFs
- New function `validate_pdf_file(path)` in `core/utils.py`

### 🔧 Changed

- Added PDF validation checks inside `core/` functions
- Improved separation of concerns:
  - `core/` handles logic only
  - `gui/` manages user interaction, logging, and feedback

---

## [v0.1.0] – 2025-06-11

### ✨ Added

- Initial version of the PDF tool
- Core functionality:
  - Merge PDFs (`core/pdf_merge.py`)
  - Split PDFs (`core/pdf_splitter.py`)
  - Rename PDFs (`core/pdf_rename.py`)
- GUI implemented using Tkinter:
  - Merge, Split, Rename interfaces
  - Main window and navigation (`gui/main_window.py`)
- Logging system in place (`logs/user_activity.log`)
- Configuration management via `config/config.py`
- Operations return a structured `Result` object with `success`, `error_type`, and `message`
- GUI components display error messages using `gui/error_handler_gui.py`
- GUI components also handle logging of failed/successful operations
