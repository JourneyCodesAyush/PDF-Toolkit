# Batch Operations GUI (CustomTkinter)

import os

import customtkinter as ctk
from PIL import Image

from core.utils import get_absolute_path
from gui.batch.batch_merge_gui import batch_merge_pdf_gui
from gui.batch.batch_rename_gui import batch_rename_pdf_gui
from gui.batch.batch_split_gui import batch_split_pdf_gui
from gui.common_ui import load_icon_safe
from gui.error_handler_gui import show_message
from version import __version__


def batch_operations_gui_window(parent=None):
    window = ctk.CTkToplevel(parent)
    window.title(f"PDF Toolkit v{__version__}")
    window.geometry("800x500")
    window.minsize(800, 500)
    window.transient(parent)
    window.grab_set()
    window.focus_set()

    icon_result = load_icon_safe(window)
    if not icon_result.success and icon_result.error_type == "warning":
        show_message(icon_result)

    # Fonts
    FONT_TITLE = ctk.CTkFont("Helvetica", size=22, weight="bold")
    FONT_DESC = ctk.CTkFont("Helvetica", size=12)
    FONT_BUTTON = ctk.CTkFont("Helvetica", size=13)
    FONT_FOOTER = ctk.CTkFont("Helvetica", size=12)

    # Layout config
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Header
    header = ctk.CTkFrame(window, height=60, fg_color="transparent")
    header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
    header.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(
        header,
        text="📁 Batch Operations",
        font=FONT_TITLE,
        anchor="w",
    )
    title.grid(row=0, column=0, sticky="w")

    # Body
    body = ctk.CTkFrame(window, fg_color="transparent")
    body.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
    body.grid_columnconfigure((0, 1), weight=1, uniform="a")
    body.grid_rowconfigure(0, weight=1)

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
        card.grid_rowconfigure((0, 1, 2), weight=1)
        card.grid_columnconfigure(0, weight=1)

        # Image
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(48, 48))
        image_label = ctk.CTkLabel(card, image=image, text="")
        image_label.grid(row=0, column=0, pady=(10, 4), sticky="n")

        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=desc,
            font=FONT_DESC,
            wraplength=240,
            justify="center",
        )
        desc_label.grid(row=1, column=0, padx=10, pady=4, sticky="n")

        # Button
        open_btn = ctk.CTkButton(card, text="Open", command=command)
        open_btn.grid(row=2, column=0, pady=(0, 10), sticky="s")

        return card

    cards = [
        (
            get_absolute_path(os.path.join("assets", "merge_file.png")),
            "Merge all PDFs from a folder into one file.",
            lambda: batch_merge_pdf_gui(window),
        ),
        (
            get_absolute_path(os.path.join("assets", "rename_file.png")),
            "Rename all PDFs in a folder using custom rules.",
            lambda: batch_rename_pdf_gui(window),
        ),
        (
            get_absolute_path(os.path.join("assets", "split_file.png")),
            "Split a PDF into single-paged files in batch.",
            lambda: batch_split_pdf_gui(window),
        ),
    ]

    for idx, (img, desc, cmd) in enumerate(cards):
        row, col = divmod(idx, 2)
        card = create_card(body, img, desc, cmd)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    # Footer
    footer = ctk.CTkFrame(window, height=30, fg_color="transparent")
    footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
    footer.grid_columnconfigure(0, weight=1)

    footer_label = ctk.CTkLabel(
        footer, text="© 2025 JourneyCodesAyush", font=FONT_FOOTER
    )
    footer_label.grid(row=0, column=0, sticky="e")


if __name__ == "__main__":
    batch_operations_gui_window()
