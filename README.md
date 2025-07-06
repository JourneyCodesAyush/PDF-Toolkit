# PDF Toolkit – Prototype (Archived)

![Python](https://img.shields.io/badge/python-3.6%2B-blue) ![Platform](https://img.shields.io/badge/platform-Windows--Linux--macOS-lightgrey)  ![Status](https://img.shields.io/badge/status-archived-lightgrey)

> ⚠️ This is an early prototype version (v0.1) that is **archived** and will not receive updates.  
> Please refer to the [main branch](https://github.com/JourneyCodesAyush) for the latest stable releases and active development.

---

This is the first working prototype of PDF Toolkit — a lightweight desktop app built with Python and Tkinter — that supports basic PDF operations like merging, renaming, and splitting files.

---

## Features

- Merge multiple PDF files into one
- Rename a selected PDF file
- Split a PDF file into specific page ranges

---

## Requirements

- Python 3.6 or higher
- PyPDF2

Install required package:

```bash
pip install -r requirements.txt
```

---

## How to Run

1. Download the repository or clone this branch.
2. Open a terminal in the project folder.
3. Run the app:


```bash
python Project_PDF.py
```

---

## Usage

### Merge PDFs
- Click "Select files here" under "Want to merge some PDFs?"
- Choose multiple PDFs.
- Choose where to save the merged file.

### Rename PDF
- Click "Select file here" under "Want to rename a PDF?"
- Choose a PDF file.
- Enter the new name when prompted.

### Split PDF
- Click "Select file here" under "Want to split a PDF?"
- Choose a PDF file.
- Input page ranges (e.g., `1-3,5,7-9`).
- Choose where to save the split files.

---

## File Structure

``` python
main.py # GUI-based prototype script
README.md # This file
```

---

## License

MIT License  
© 2025 JourneyCodesAyush

---

## Author

Created by JourneyCodesAyush  
Crafted with care and lots of ❤️ 
GitHub: https://github.com/JourneyCodesAyush