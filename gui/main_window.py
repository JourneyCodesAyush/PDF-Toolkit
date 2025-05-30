# GUI window code

import os
from tkinter import Tk, RAISED, Label, Button
from config.config import setup_logger
from gui.merge_gui import mergePDF_GUI
from gui.rename_gui import rename_file_gui
from gui.split_gui import split_pdf_gui

logger = setup_logger(__name__)


def main():
    """
    Main window of the application
    """
    root = Tk()
    root.title(os.getcwd())
    root.geometry("544x344")
    root.resizable(width=False, height=False)

    Label(root, text="Want to merge some PDFs?", font="helvetica").grid(
        row=0, column=1, padx=5, pady=5
    )

    widget = Button(root, text="Select files here", relief=RAISED, command=mergePDF_GUI)
    widget.grid(row=0, column=2)

    Label(root, text="Want to rename a PDF?", font="helvetica").grid(
        row=2, column=1, padx=5, pady=5
    )
    widget = Button(
        root, text="Select file here", relief=RAISED, command=rename_file_gui
    )
    widget.grid(row=2, column=2)

    Label(root, text="Want to split a PDF?", font="helvetica").grid(
        row=4, column=1, padx=5, pady=5
    )
    widget = Button(root, text="Select file here", relief=RAISED, command=split_pdf_gui)
    widget.grid(row=4, column=2)

    root.mainloop()


if __name__ == "__main__":
    main()
