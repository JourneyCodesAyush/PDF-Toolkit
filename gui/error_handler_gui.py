# Showing error to the user

from tkinter import messagebox


def show_message(msg: dict):
    """
    Shows errors to the user via GUI
    """
    if msg["error_type"] == "error":
        messagebox.showerror(title=msg["title"], message=msg["message"])
    elif msg["error_type"] == "warning":
        messagebox.showwarning(title=msg["title"], message=msg["message"])
    else:
        messagebox.showinfo(title=msg["title"], message=msg["message"])
