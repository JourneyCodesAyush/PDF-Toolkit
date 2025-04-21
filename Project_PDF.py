from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfWriter, PdfMerger, PdfReader
import os


def mergePDF():
    # print("You are now in 'mergePDF' function!")
    file_path = filedialog.askopenfilenames(
        title="Select PDFs to merge",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )
    # print(file_path)
    # print(f"Selected files: {file_path}")
    # merger = PdfWriter()  # This is not the correct method to merge PDFs
    merger = PdfMerger()  # This is the CORRECT one
    if not file_path:
        print("No file selected")
        messagebox.showerror(title="Error", message="No PDF files selected!")
        return
    else:
        for pdf in file_path:
            if pdf.lower().endswith(".pdf"):
                merger.append(pdf)
            else:
                messagebox.showinfo(
                    title="Invalid", message=f"Invalid file format: {pdf}"
                )
                continue
        save_file_path = filedialog.asksaveasfilename(
            title="Where do you want to save the file?",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension=".pdf",
        )

        if not save_file_path:
            messagebox.showinfo(
                title="Error", message="Please provide valid output location"
            )
            return
        merger.write(save_file_path)
        merger.close()
        messagebox.showinfo(
            title="Result",
            message=f"PDF files have been successfully merged at location {save_file_path}",
        )


def rename_file():
    old_file_name = filedialog.askopenfilename(
        title="Select PDFs to rename",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )
    if not old_file_name:
        messagebox.showwarning(
            title="Warning", message="Please select a file to rename."
        )
    else:
        new_file_name = simpledialog.askstring(
            title="NewName", prompt="Input new name: "
        )
        os.rename(old_file_name, f"{new_file_name}.pdf")
        messagebox.showinfo(
            title="Success",
            message=f"File at {old_file_name} renamed to {new_file_name}",
        )


def split_pdf_custom():
    file_name = filedialog.askopenfilename(
        title="Select PDF to split",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )
    if not file_name:
        messagebox.showwarning(
            title="Warning", message="Please select a file to rename."
        )
    else:
        page_range_input = simpledialog.askstring(
            title="PDF splitting", prompt="Enter the page number (e.g. 1-3,4,5-7)"
        )
        if page_range_input is None:
            messagebox.showerror(title="Error", message="Please enter a range")
            return
        page_range_strings = page_range_input.split(",")
        # print(page_range)
        page_range = []
        for each in page_range_strings:
            # page_range.append(tuple(each.split("-")))
            each = each.strip()
            if "-" in each:
                start, end = each.split("-")
                # start = int(start)
                # end = int(end)
                page_range.append((int(start), int(end)))
            else:
                page_range.append((int(each), int(each)))
        # print(page_range)

        save_file_path = filedialog.askdirectory(
            title="Select folder to save the splitted files?"
        )

        if not save_file_path:
            messagebox.showinfo(title="No folder", message="Output folder not selected")
            return

        reader = PdfReader(file_name)
        for start, end in page_range:
            writer = PdfWriter()
            for i in range(start - 1, end):
                if i < len(reader.pages):
                    writer.add_page(reader.pages[i])
            if start == end:
                name = f"split_{start}.pdf"
            else:
                name = f"split_{start}-{end}.pdf"
            output_path = os.path.join(save_file_path, name)
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)

        messagebox.showinfo(
            title="Successful!",
            message=f"Files have been successfully saved to location {save_file_path}\n",
        )


root = Tk()
root.title(os.getcwd())
root.geometry("544x344")
root.resizable(width=False, height=False)

Label(root, text="Want to merge some PDFs?", font="helvetica").grid(
    row=0, column=1, padx=5, pady=5
)

widget = Button(root, text="Select files here", relief=RAISED, command=mergePDF)
widget.grid(row=0, column=2)
# widget.bind("<Button-1>", mergePDF)


Label(root, text="Want to rename a PDF?", font="helvetica").grid(
    row=2, column=1, padx=5, pady=5
)
widget = Button(root, text="Select file here", relief=RAISED, command=rename_file)
widget.grid(row=2, column=2)
# widget.bind("<Button-1>", rename_file)

Label(root, text="Want to split a PDF?", font="helvetica").grid(
    row=4, column=1, padx=5, pady=5
)
widget = Button(root, text="Select file here", relief=RAISED, command=split_pdf_custom)
widget.grid(row=4, column=2)
# widget.bind("<Button-1>", rename_file)


root.mainloop()
