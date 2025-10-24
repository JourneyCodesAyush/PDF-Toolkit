# Shared UI

import json
import os
import threading
from pathlib import Path
from tkinter import PhotoImage, messagebox, ttk
from typing import Callable

import customtkinter as ctk

import core.globals
from config.preferences_manager import USER_PREFERENCES, get_preferences
from core.error_handler import create_msg_object
from core.globals import ENCRYPTED_FILE_HANDLING, EncryptedFileHandling
from core.result import Result
from core.utils import get_absolute_path
from gui.encrypted_pdf_frame import EncryptedPdfFrame
from gui.error_handler_gui import show_message


def load_icon_safe(root) -> Result:
    """
    Load and set the application icon for the given Tkinter root window safely.

    Args:
        root (tk.Tk): The root Tkinter window instance to set the icon on.

    Returns:
        Result: Indicates success or failure of loading the icon, with message and error type.

    Behavior:
        Attempts to locate the icon file via an absolute path and set it as the window icon.
        If the icon file is missing or cannot be loaded, returns a warning Result explaining the issue.
    """
    try:
        # ICON_PATH = get_absolute_path("../assets/PDF_file.ico")
        ICON_PATH = get_absolute_path(os.path.join("assets", "PDF_file.png"))
        if not os.path.exists(ICON_PATH):
            raise FileNotFoundError(f"Icon not found at: {ICON_PATH}")

        icon_image = PhotoImage(file=ICON_PATH)
        root.iconphoto(True, icon_image)
        # root.iconbitmap(ICON_PATH)

        return Result(
            success=True,
            title="Icon Loaded",
            message="App Icon loaded successfully.",
            error_type="info",
        )
    except Exception as e:
        return Result(
            success=False,
            title="Icon load failed",
            message=f"Could not load app icon.\nUsing default icon.\n\nDetails: {str(e)}",
            error_type="warning",
        )


class ProgressBar(ctk.CTkToplevel):
    """
    Modal progress bar window that shows an indeterminate progress animation,
    optionally switching to a password prompt when needed.

    Args:
        master (ctk.CTk): The parent customtkinter window to which this modal belongs.

    Returns:
        None: This class represents a window and does not return a value.

    Behavior:
        - Displays a modal indeterminate progress bar while a task is running.
        - Disables interaction with the parent window (via grab_set()).
        - Can switch to a password input frame for encrypted PDF files.
        - Automatically destroys itself when stopped.
    """

    def __init__(self, master: ctk.CTk | ctk.CTkToplevel) -> None:
        if master is None:
            raise ValueError("ProgressBar requires a master customtkinter window.")
        super().__init__(master=master)

        self.title("Please wait...")
        self.geometry("400x200")
        self.minsize(400, 200)
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.transient(master)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # Container frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both")

        # Progress widgets
        self.label = ttk.Label(self.content_frame, text="Processing... Please wait.")
        self.progress_bar = ttk.Progressbar(
            self.content_frame, mode="indeterminate", orient="horizontal", length=360
        )
        self.label.pack(pady=(30, 10))
        self.progress_bar.pack(pady=(0, 30), padx=20, fill="x")

        # Password frame reference
        self.password_frame = None

    def start(self) -> None:
        """
        Begin showing the progress animation and ensure UI is in progress mode.
        """
        self.show_progress()
        self.progress_bar.start()

    def stop(self) -> None:
        """
        Stop the progress animation and close the modal progress window.
        """
        self.progress_bar.stop()
        self.destroy()

    def show_progress(self) -> None:
        """
        Switch UI back to progress mode by hiding any password prompt and showing the progress bar.
        """

        if self.password_frame:
            self.password_frame.pack_forget()
            self.password_frame.destroy()
            self.password_frame = None
        self.label.pack(pady=(30, 10))
        self.progress_bar.pack(pady=(0, 30), padx=20, fill="x")
        self.progress_bar.start()

    def show_password_prompt(
        self, filename: str, on_complete: Callable[[tuple[str, str | None]], None]
    ):
        """
        Display a password prompt in place of the progress bar.

        Args:
            filename (str): The name of the encrypted PDF requiring a password.
            on_complete (Callable): Callback to return the entered password or skip action.
        """
        self.progress_bar.stop()
        self.label.pack_forget()
        self.progress_bar.pack_forget()

        self.password_frame = EncryptedPdfFrame(
            master=self.content_frame, filename=filename, on_complete=on_complete
        )
        self.password_frame.pack(expand=True, fill="both", padx=10, pady=10)


def run_task_with_progress(
    root: ctk.CTk | ctk.CTkToplevel,
    task_func: Callable[[ProgressBar], Result],
    on_done=Callable[[Result], None],
) -> None:
    """
    Run a background task while showing an indeterminate progress bar modal.

    Args:
        root (ctk.CTk): The root window used to attach the progress modal.
        task_func (Callable[[ProgressBar], Result]): The function representing the long-running task. It receives the progress bar and returns a Result.
        on_done (Callable[[Result], None]): Callback to execute on the main thread after task completion.

    Returns:
        None

    Behavior:
        - Creates and displays a modal ProgressBar.
        - Executes task_func() in a background thread while showing the progress animation.
        - After task completion, closes the modal and calls on_done() with the result on the main thread.
    """
    progress = ProgressBar(root)
    progress.start()

    def worker():
        result = task_func(progress)

        def finish():
            progress.stop()
            on_done(result)

        root.after(0, finish)

    threading.Thread(target=worker, daemon=True).start()


def save_preferences():
    """
    Prompt the user to save their preferences and update the preferences file accordingly.

    Prompts the user with a Yes/No dialog asking whether they want to save their preferences.
    The user's choice is then stored in the preferences JSON file.

    Returns:
        None: This function performs file operations and user interaction but does not return a value.

    Behaviour:
        - Displays a confirmation dialog to the user.
        - If the user confirms, updates the save_preferences key in the preferences file.
        - Handles any exceptions during file writing and shows an error message if needed.
    """

    save_or_not = messagebox.askyesno(
        title="Preferences", message="Do you want to save the preferences?"
    )

    prefs = get_preferences()
    prefs["save_preferences"] = save_or_not
    try:
        with open(USER_PREFERENCES, mode="w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=4)
    except Exception as e:
        show_message(
            create_msg_object(
                error_type="Unknown", title="Some error occurred", message=f"{str(e)}"
            )
        )


def ask_password(
    file: str, progress_window: ProgressBar, on_result: Callable[[str | None], None]
) -> str | None:
    """
    Display a password prompt for an encrypted PDF and handle user input.

    Args:
        file (str): The full path of the encrypted PDF file.
        progress_window (ProgressBar): The modal progress window that displays while waiting for the user to enter the password.
        on_result (Callable[[str | None], None]): Callback function that is called when the user provides a password or skips the prompt. It receives the entered password (str) or None if the user skips.

    Behavior:
        - If the global setting ENCRYPTED_FILE_HANDLING is set to SKIP_ALL, the password prompt is skipped entirely,
          and None is returned via the callback.
        - Displays a modal asking for the password, with options to either enter a password, skip this file, or skip all future prompts.
        - Updates the ENCRYPTED_FILE_HANDLING global setting based on the user's choice:
            - "password" action: passes the entered password to the callback.
            - "skip" action: skips the current file and continues without a password.
            - "skip_all" action: suppresses future password prompts for all encrypted PDFs.
        - If the prompt is dismissed or cancelled, the progress window will reappear.
    """

    global ENCRYPTED_FILE_HANDLING

    if ENCRYPTED_FILE_HANDLING == EncryptedFileHandling.SKIP_ALL:
        on_result(None)
        return

    filename = Path(file).name

    def handle_response(result: tuple[str, str | None]):
        """
        Handle the result of the password prompt interaction.

        Args:
            result (tuple[str, str | None]): A tuple where the first element is the action string
                                             ("password", "skip", "skip_all"), and the second is
                                             the entered password or None.

        Behavior:
            - If action is "password": pass the password to the callback.
            - If action is "skip": update the global handling mode to SKIP and continue without a password.
            - If action is "skip_all": set the handling mode to SKIP_ALL to suppress future prompts.
            - If none match: return to progress view without taking action.
        """

        action, data = result
        if action == "password":
            on_result(data)
        if action == "skip":
            core.globals.ENCRYPTED_FILE_HANDLING = EncryptedFileHandling.SKIP
            on_result(None)
            return
        if action == "skip_all":
            core.globals.ENCRYPTED_FILE_HANDLING = EncryptedFileHandling.SKIP_ALL
            on_result(None)
            return
        progress_window.show_progress()

    progress_window.show_password_prompt(filename=filename, on_complete=handle_response)


def make_gui_password_callback(progress_window: ProgressBar):
    """
    Create a synchronous password prompt callback for encrypted PDF handling.

    Args:
        progress_window (ProgressBar): The active progress modal window where password prompt will be displayed.

    Returns:
        Callable[[str], str | None]: A callback function to be passed into core/ functions.
                                     It takes a file path and returns the password or None.

    Behavior:
        - Wraps the asynchronous ask_password() GUI flow into a synchronous-style callback.
        - Uses a threading.Event() to block until the user responds to the password prompt.
        - Stores and returns the user input once available.
    """

    def callback(file_path: str) -> str | None:
        """
        Prompt the user for a password and block until a response is received.

        Args:
            file_path (str): The full path to the encrypted PDF requiring a password.

        Returns:
            str | None: The entered password, or None if skipped.

        Behavior:
            - Initiates an asynchronous password prompt using ask_password().
            - Uses a threading.Event() to block execution until the user responds.
            - Captures the result in a shared dictionary and returns it once available.
        """

        event = threading.Event()
        password_container: dict[str, str | None] = {"value": None}

        def on_password_result(password: str | None = None):
            """
            Store the entered password and signal completion of the password prompt.

            Args:
                password (str | None): The password entered by the user, or None if the user chose to skip.

            Behavior:
                - Saves the password result into a shared dictionary (password_container).
                - Triggers the threading event to unblock the waiting callback() function.
            """
            password_container["value"] = password
            event.set()

        ask_password(file_path, progress_window, on_password_result)
        event.wait()
        return password_container["value"]

    return callback
