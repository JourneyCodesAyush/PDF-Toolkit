# Shared UI

import os
import threading
import tkinter as tk
from tkinter import Toplevel, ttk
from typing import Callable, Union

from core.result import Result
from core.utils import get_absolute_path


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
        ICON_PATH = get_absolute_path(os.path.join("assets", "PDF_file.ico"))
        if not os.path.exists(ICON_PATH):
            raise FileNotFoundError(f"Icon not found at: {ICON_PATH}")
        root.iconbitmap(ICON_PATH)
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


class ProgressBar(Toplevel):
    """
    Modal progress bar window that shows an indeterminate progress animation.

    Args:
        master (tk.Tk): The parent Tkinter root window on which to create this modal progress bar.

    Returns:
        None: This class represents a window and does not return a value.

    Behaviour:
        Creates a small modal window that disables interaction with the main window.
        Shows an indeterminate progress bar animation until stopped.
    """

    def __init__(self, master: tk.Tk) -> None:
        if master is None:
            raise ValueError("ProgressBar requires a master Tkinter window.")
        super().__init__(master=master)

        self.title("Please wait...")
        self.geometry("400x150")
        self.minsize(400, 150)
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.transient(master)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", lambda: None)

        self.label = ttk.Label(self, text="Processing... Please wait.")
        self.label.pack(pady=(30, 10))

        self.progress_bar = ttk.Progressbar(
            self, mode="indeterminate", orient="horizontal", length=360
        )

        self.progress_bar.pack(pady=(0, 30), padx=20, fill="x")

    def start(self) -> None:
        self.progress_bar.start()

    def stop(self) -> None:
        self.progress_bar.stop()
        self.destroy()


def run_task_with_progress(
    root: Union[tk.Tk, tk.Toplevel],
    task_func: Callable[[], Result],
    on_done=Callable[[Result], None],
) -> None:
    """
    Run a long-running task in a background thread while showing a modal progress bar.

    Args:
        root (tk.Tk): The parent Tkinter root window used for creating the progress bar modal window.
        task_func (Callable[[], Result]): The function representing the long-running task. Should return a Result object.
        on_done (Callable[[Result], None]): A callback function that will be called with the Result from task_func upon completion.

    Returns:
        None: This function manages GUI updates and threading internally, returning no value.

    Behaviour:
        Displays a modal ProgressBar window and starts its animation.
        Runs task_func in a separate thread to keep the GUI responsive.
        When task_func completes, schedules stopping the progress bar and calls on_done with the result on the main thread.
    """
    progress = ProgressBar(root)
    progress.start()

    def worker():
        result = task_func()

        def finish():
            progress.stop()
            on_done(result)

        root.after(0, finish)

    threading.Thread(target=worker, daemon=True).start()
