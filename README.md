# PDF Toolkit – Prototype with Logging (Archived)

![Python](https://img.shields.io/badge/python-3.6%2B-blue) ![Platform](https://img.shields.io/badge/platform-Windows--Linux--macOS-lightgrey)  ![Status](https://img.shields.io/badge/status-archived-lightgrey)

> ⚠️ This is an early prototype version (v0.2) that is **archived** and will not receive updates.  
> Please refer to the [main branch](https://github.com/JourneyCodesAyush) for the latest stable releases and active development.

---

This prototype builds upon the first version by adding detailed **logging functionality** to track user actions and errors during PDF operations.

---

## Features

- Merge multiple PDF files into one, with logging of success and error events
- Rename a selected PDF file, with logging of operations and error handling
- Split a PDF file into specific page ranges, with logging of the split operations and errors

---

## Requirements

- Python 3.6 or higher
- PyPDF2

**Install required package**:

**On Windows**
```bash
pip install -r requirements.txt
```
**On Linux/Mac**
```bash
pip3 install -r requirements.txt
```

## How to Run

1. Download the repository or clone this branch.
2. Open a terminal in the project folder.
3. Run the app: 
**On Windows**
```bash
python Project_PDF.py
```
**On Linux/Mac**
```bash
python3 Project_PDF.py
```

---

## Usage

### Merge PDFs
- Click `Select files here` under `Want to merge some PDFs?`
- Choose multiple PDFs.
- Choose where to save the merged file.
- Logs will be recorded in `user_activity.log`.

### Rename PDF
- Click `Select files here` under `Want to rename a PDF?`
- Choose a PDF file.
- Enter the new name when prompted.
- Logs of success and failures will be recorded.

### Split PDF
- Click `Select files here` under `Want to split a PDF?`
- Choose a PDF file.
- Input page ranges (e.g. `1-3,5,7-9`).
- Choose where to save the split files.
- All activities and errors will be logged.

---

## File Structure

```python
Project_PDF.py # GUI-based prototype script with logging
README.md # You're here
logs/user_activity.log # Log file generated during usage
```

---

## LICENSE
MIT License
© 2025 JourneyCodesAyush

---

## Author 
Created by JourneyCodesAyush
Crafted with care and lots of ❤️
GitHub: https://github.com/JourneyCodesAyush