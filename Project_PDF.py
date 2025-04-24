# 20th April 2025
# Started at around 10 AM
# 21st April 2025
# Aaj ke din PDF splitting wala function implement kiya. Ab logging implement karna hai
# "logging" module ka istemal karke

from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfWriter, PdfMerger, PdfReader
import os
import logging

logging.basicConfig(filename="user_activity.log",level= logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",encoding='utf-8')

def mergePDF():
    logging.info("Merge PDF operation started")
    # print("You are now in 'mergePDF' function!")
    file_path = filedialog.askopenfilenames(
        title="Select PDFs to merge",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )
    # print(file_path)
    # print(f"Selected files: {file_path}")
    # merger = PdfWriter()  # This is not the correct method to merge PDFs
    if not file_path:
        print("No file selected")
        messagebox.showerror(title="Error", message="No PDF files selected!")
        logging.warning("Merging failed - No file selected")
        return
    
    merger = PdfMerger()  # This is the CORRECT one
    for pdf in file_path:
        try:
            if pdf.lower().endswith(".pdf"):
                merger.append(pdf)
            else:
                messagebox.showinfo(
                title="Invalid", message=f"Invalid file format: {pdf}"
                )
                logging.warning(f"Merging failed - Invalid file format: {pdf}")
                continue
        except FileNotFoundError:
                messagebox.showerror(
                title="File Not Found",
                message=f"Merging failed - file NOT found: {pdf}",
            )
                logging.error(f"Merging failed - {pdf} NOT found")
        except PermissionError:
                messagebox.showerror(
                title="Permission Error",
                message=f"Permisson denied for: {pdf}",
            )
                logging.error(f"Merging failed - Permission denied: {pdf}")
        except OSError as e:
                messagebox.showerror(title="OS Error", message=f"An OS Error occurred: {e}")
                logging.error(f"Merging failed - OS Error: {e}")
        except Exception as e:
                messagebox.showerror(title="Unexpected Error",message=f"An unexpected error occurred: {e}")
                logging.error(f"Merging failed - Unexpected error: {e}")

    if not merger.pages:
        logging.warning("Merging failed - No valid PDFs were selected")
        messagebox.showinfo(title="No Valid PDFs",message= "No valid PDFs were selected to merge.")
        return
    
    try:
        save_file_path = filedialog.asksaveasfilename(
            title="Where do you want to save the file?",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
            defaultextension=".pdf",
        )

        if not save_file_path:
            messagebox.showinfo(
                title="Error", message="Please provide valid output location"
            )
            logging.warning("Merging failed - Output file name NOT selected")
            return
        
        merger.write(save_file_path)
        merger.close()
        messagebox.showinfo(
            title="Result",
            message=f"PDF files have been successfully merged at location {save_file_path}",
        )
        logging.info(f"PDF merged and saved at {save_file_path}")

    except PermissionError:
        messagebox.showerror(
                title="Permission Error",
                message=f"Permisson denied to save merged PDF",
            )
        logging.error(f"Merging aborted - Permisson denied to save merged PDF")
    except OSError as e:
            messagebox.showerror(title="OS Error", message=f"An OS Error occurred: {e}")
            logging.error(f"Merging aborted - Error while saving the merged PDF: {e}")
    except Exception as e:
            messagebox.showerror(title="Unexpected Error",message=f"An unexpected error occurred: {e}")
            logging.error(f"Merging aborted - Unexpected error while saving: {e}")

    


def rename_file():
    logging.info("Rename PDF operation started")
    old_file_name = filedialog.askopenfilename(
        title="Select PDFs to rename",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )
    if not old_file_name:
        messagebox.showwarning(
            title="Warning", message="Please select a file to rename."
        )
        return;
    
    new_directory = filedialog.askdirectory(title="Select a directory to save the renamed PDF")
    if not new_directory:
        messagebox.showwarning(
            title="Warning", message="Please select a directory to save the file into"
        )
        return;
    new_file_name = simpledialog.askstring(
        title="NewName", prompt="Input new name: "
        )

    if not new_file_name or not new_file_name.strip():
        messagebox.showwarning(title="Invalid name!",message="Please enter a valid file name")
        return;
    new_file_name = new_file_name.strip()

    if not new_file_name.lower().endswith(".pdf"):
        new_file_name += ".pdf"

    new_file_path = os.path.join(new_directory,f"{new_file_name}")

    if os.path.exists(new_file_path):
        messagebox.showerror(title="File Exists",message=f" A file named {new_file_name} already exists in the selected directory")
        logging.warning(f"Rename aborted - file exists: {new_file_path}")
        return
    try:
        os.rename(old_file_name, new_file_path)
        messagebox.showinfo(
                title="Success",
                message=f"File at {old_file_name} renamed to {new_file_name}",
            )
        logging.info(f"{old_file_name} PDF renamed to {new_file_name}")
    except FileNotFoundError:
        messagebox.showerror(
                title="Error!",
                message=f"Rename failed - file NOT found: {old_file_name}",
            )
        logging.error(f"Rename failed - {old_file_name} NOT found")
    except PermissionError:
        messagebox.showerror(
                title="Permission Error",
                message=f"Permisson denied to access the given file",
            )
        logging.error(f"Rename failed - Permission denied: {old_file_name} to {new_file_path}")
    except OSError as e:
        messagebox.showerror(title="OS Error", message=f"An OS Error occurred: {e}")
        logging.error(f"Rename failed - OS Error: {e}")
    except Exception as e:
        messagebox.showerror(title="Unexpected Error",message=f"An unexpected error occurred: {e}")
        logging.error(f"Rename aborted - Unexpected error: {e}")


def parse_page_ranges(page_range_input,total_pages):
    page_range_strings = page_range_input.split(",")
    # print(page_range)
    page_range = []
    for each in page_range_strings:
        each = each.strip()
        try:
            if "-" in each:
                start,end = each.split("-")
                start, end = map(int,[start,end])
                if start > end:
                    raise ValueError("Start page cannot be greater than end page")
            else:
                start = end = int(each)

            if start < 1 or end > total_pages:
                raise IndexError("Page range out of bounds")
                
            page_range.append((int(start), int(end)))
        except ValueError as ve:
            messagebox.showerror(title="Invalid Range",message=f"Error: {ve}")
            return None
        except IndexError as ie:
            messagebox.showerror(title="Invalid Range",message=f"Error: {ie}")
            return None
        except Exception as e:
            messagebox.showerror(title="Invalid Range",message=f"Error: {e}")
            return None              
    return page_range    


def split_pdf_custom():
    logging.info("Split PDF operation started")
    file_name = filedialog.askopenfilename(
        title="Select PDF to split",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.pdf")],
        defaultextension="*.pdf",
    )
    if not file_name:
        messagebox.showwarning(
            title="Warning", message="Please select a file to rename."
        )
        logging.warning("No PDF file selected to split")
        return
    try:
        page_range_input = simpledialog.askstring(
            title="PDF splitting", prompt="Enter the page number (e.g. 1-3,4,5-7)"
            )
        if not page_range_input :
            messagebox.showerror(title="Error", message="Please enter a range")
            logging.warning("No valid page range entered")
            return
        
        reader = PdfReader(file_name)
        total_pages = len(reader.pages)
        page_range = parse_page_ranges(page_range_input,total_pages)

        if page_range is None:
            return

        save_file_path = filedialog.askdirectory(
                title="Select folder to save the splitted files?"
            )

        if not save_file_path:
                messagebox.showinfo(title="No folder", message="Output folder not selected")
                logging.warning("No folder selected to save split files")
                return

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

            try:
                with open(output_path, "wb") as output_pdf:
                    writer.write(output_pdf)

            except PermissionError:
                messagebox.showerror(title="Permission error",message=f"Permission denied for saving: {output_path}")
                logging.error(f"Permission denied for saving: {output_path}")
                return
            except OSError as e:
                messagebox.showerror(title="OS error",message=f"An OS Error occurred: {e}")
                logging.error(f"OS Error while saving: {output_path} - {e}")
                return
            
            except Exception as e:
                messagebox.showerror(title="Unexpected error",message=f"An unexpected error occurred: {e}")
                logging.error(f"Unexpected Error while saving: {output_path} - {e}")
                return
            

        messagebox.showinfo(
                title="Successful!",
                message=f"Files have been successfully saved to location {save_file_path}\n",
            )
        logging.info(f"{file_name} PDF splitted into PDFs range {page_range}")
    except Exception as e:
        messagebox.showerror(title="Unexpected error",message=f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected Error with file: {file_name} - {e}")
        return
         

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
