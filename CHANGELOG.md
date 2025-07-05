# 📄 Changelog

All notable changes to this project will be documented in this file.

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) guidelines and uses [Semantic Versioning](https://semver.org/).

---

## [v0.4.1] – 2025-07-05

### 🐞 Fixed
- Replace `.ico` icon with `.png` to improve compatibility with Linux desktop environments.

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

## [v0.1.0] – 2025-05-11

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
