# Showing error to the user

from tkinter import messagebox
from core.result import Result


def show_message(result: Result):
    """
    Shows messages to the user via GUI based on the Result object.
    """
    if result.error_type == "error":
        messagebox.showerror(title=result.title, message=result.message)
    elif result.error_type == "warning":
        messagebox.showwarning(title=result.title, message=result.message)
    else:
        messagebox.showinfo(title=result.title, message=result.message)
