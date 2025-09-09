# GUI window code


import os
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from core.utils import get_persistent_path
from gui.batch.batch_operations_gui import batch_operations_gui_window
from gui.common_ui import save_preferences
from gui.extract_page_pdf import extract_page_pdf_gui
from gui.merge_gui import merge_pdf_gui
from gui.rename_gui import rename_file_gui
from gui.split_gui import split_pdf_gui
from version import __version__

ctk.set_appearance_mode("Light")  # Dark, Light, System
ctk.set_default_color_theme("dark-blue")


def main():
    root = ctk.CTk()
    root.geometry("800x600")
    root.minsize(1000, 680)
    root.title(f"PDF Toolkit v{__version__}")

    # Font constants
    FONT_TITLE = ctk.CTkFont("Helvetica", size=24, weight="bold")
    FONT_DESC = ctk.CTkFont("Helvetica", size=12)
    FONT_BUTTON = ctk.CTkFont("Helvetica", size=13)
    FONT_FOOTER = ctk.CTkFont("Helvetica", size=12)

    # Configure grid layout
    root.grid_rowconfigure(1, weight=1)  # Body
    root.grid_columnconfigure(0, weight=1)

    # Header
    header = ctk.CTkFrame(root, height=60, fg_color="transparent")
    header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)

    title = ctk.CTkLabel(
        header,
        text="📄 PDF Toolkit",
        font=FONT_TITLE,
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="w")

    pref_btn = ctk.CTkButton(
        header,
        text="⚙",
        width=40,
        command=save_preferences,
        fg_color="#000000",
        hover_color="#242424",
        font=FONT_BUTTON,
    )
    pref_btn.grid(row=0, column=1, sticky="e")

    # Body
    body = ctk.CTkFrame(root, fg_color="transparent")
    body.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
    body.grid_columnconfigure((0, 1), weight=1, uniform="a")
    body.grid_rowconfigure((0, 1), weight=1, uniform="a")

    def create_card(parent, image_path, desc, command):
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            border_width=1,
            border_color="#A9A9A9",
            fg_color="#f4f4f4" if ctk.get_appearance_mode() == "Light" else "#2b2b2b",
        )
        card.grid_propagate(False)
        card.configure(width=300, height=200)

        # Layout for the card itself
        card.grid_rowconfigure((0, 1, 2), weight=1)
        card.grid_columnconfigure(0, weight=1)

        # Image
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(48, 48))
        image_label = ctk.CTkLabel(card, image=image, text="")
        image_label.grid(row=0, column=0, pady=(10, 4), sticky="n")

        # Description
        desc_label = ctk.CTkLabel(
            card, text=desc, font=FONT_DESC, wraplength=240, justify="center"
        )
        desc_label.grid(row=1, column=0, padx=10, pady=4, sticky="n")

        # Button
        open_btn = ctk.CTkButton(card, text="Open", command=command)
        open_btn.grid(row=2, column=0, pady=(0, 10), sticky="s")

        return card

    cards = [
        (
            get_persistent_path(os.path.join("assets", "merge_file.png")),
            "Select multiple PDFs and merge them into one file.",
            lambda: merge_pdf_gui(root),
        ),
        (
            get_persistent_path(os.path.join("assets", "rename_file.png")),
            "Rename your PDFs with custom rules easily.",
            lambda: rename_file_gui(root),
        ),
        (
            get_persistent_path(os.path.join("assets", "split_file.png")),
            "Split PDFs into single or multiple pages.",
            lambda: split_pdf_gui(root),
        ),
        (
            get_persistent_path(os.path.join("assets", "extract_file.png")),
            "Extract specific pages from your PDF file.",
            lambda: extract_page_pdf_gui(root),
        ),
        (
            get_persistent_path(os.path.join("assets", "folder.png")),
            "Process multiple PDFs with batch tasks.",
            lambda: batch_operations_gui_window(root),
        ),
        (
            get_persistent_path(os.path.join("assets", "about_us.png")),
            "Learn more about this app and its developer.",
            lambda: messagebox.showinfo(
                "About", f"PDF Toolkit v{__version__}\nCreated by JourneyCodesAyush"
            ),
        ),
    ]

    for idx, (title, desc, cmd) in enumerate(cards):
        row, col = divmod(idx, 2)
        card = create_card(body, title, desc, cmd)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    footer = ctk.CTkFrame(root, height=30, fg_color="transparent")
    footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
    footer.grid_columnconfigure(0, weight=1)

    footer_label = ctk.CTkLabel(
        footer, text="© 2025 JourneyCodesAyush", font=FONT_FOOTER
    )
    footer_label.grid(row=0, column=0, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    main()
