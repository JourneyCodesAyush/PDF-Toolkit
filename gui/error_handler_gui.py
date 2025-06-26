# Showing error to the user

from tkinter import messagebox

from core.result import Result


def show_message(result: Result):
    """
    Display a message box to the user based on the Result object's status.

    Args:
        result (Result): The result object containing message details and error type.

    Behavior:
        Shows an error, warning, or info message box according to result.error_type.
    """
    if result.error_type == "error":
        messagebox.showerror(title=result.title, message=result.message)
    elif result.error_type == "warning":
        messagebox.showwarning(title=result.title, message=result.message)
    else:
        messagebox.showinfo(title=result.title, message=result.message)
