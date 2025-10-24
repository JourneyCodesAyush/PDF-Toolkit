# Frame that asks for password of the encrypted PDF

from typing import Callable

import customtkinter as ctk


class EncryptedPdfFrame(ctk.CTkFrame):
    """
    Embedded frame that prompts user to enter password for encrypted PDF.

    Args:
        master (widget): Parent CTk container (typically ProgressBar).
        filename (str): Name of the file being processed.
        on_complete (Callable): Callback function to return the result.

    Returns:
        None: Result is sent via callback in this format:
            - ("password", <user_password>)
            - ("skip", None)
            - ("skip_all", None)
    """

    def __init__(
        self,
        master: ctk.CTk | ctk.CTkFrame,
        filename: str,
        on_complete: Callable[[tuple[str, str | None]], None],
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.on_complete = on_complete

        # Title label
        ctk.CTkLabel(
            self,
            text="Encrypted PDF Detected",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=(15, 8))

        # File info
        ctk.CTkLabel(
            self,
            text=f"The file '{filename}' is password protected.\nPlease enter a password or choose to skip.",
            font=ctk.CTkFont(size=13),
            wraplength=360,
            justify="center",
        ).pack(padx=15, pady=(0, 10))

        # Password input
        self.pwd_entry = ctk.CTkEntry(self, placeholder_text="Enter password", show="*")
        self.pwd_entry.pack(padx=20, pady=10, fill="x")
        self.pwd_entry.focus_set()

        # Button group
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(2, 15))

        ctk.CTkButton(button_frame, text="Submit", command=self.submit).pack(
            side="left", padx=5
        )
        ctk.CTkButton(button_frame, text="Skip", command=self.skip).pack(
            side="left", padx=5
        )
        ctk.CTkButton(button_frame, text="Skip All", command=self.skip_all).pack(
            side="left", padx=5
        )

    def submit(self):
        """Called when user clicks 'Submit'."""
        pwd = self.pwd_entry.get()
        if not pwd:
            pass  # Automatically handled in core/
        self.on_complete(("password", pwd))

    def skip(self):
        """Skip current encrypted file."""
        self.on_complete(("skip", None))

    def skip_all(self):
        """Skip all future encrypted files."""
        self.on_complete(("skip_all", None))
