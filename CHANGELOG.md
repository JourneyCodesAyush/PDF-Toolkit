# 📄 Changelog

All notable changes to this project will be documented in this file.

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) guidelines and uses [Semantic Versioning](https://semver.org/).

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
