import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import win32com.client as win32
import openpyxl as px
from openpyxl.drawing.image import Image

def run_script():

    def select_files():
        filenames = filedialog.askopenfilenames(filetypes=(("Excel files", "*.xlsx"),))
        files_label.config(text='\n'.join(filenames))
    def reselect_files():
        files_label.config(text="")
    def convert_files():
        selected_file_paths = files_label.cget("text").split("\n")

        target_folder = filedialog.askdirectory()
        if not target_folder:
            return

        for filepath in selected_file_paths:

            excel = win32.Dispatch('Excel.Application')
            excel.Visible = False
            excel.DisplayAlerts = False

            wb = excel.Workbooks.Open(filepath)
            file_name_with_extension = os.path.basename(filepath)
            output_filepath = os.path.splitext(target_folder)[0] + "/" + os.path.splitext(file_name_with_extension)[0] + ".pdf"
            output_filepath_adj = output_filepath.replace('/', '\\')

            try:
                wb.ExportAsFixedFormat(0, output_filepath_adj)
                print(f"Converted {filepath} to PDF successfully!")
            except Exception as e:
                print(f"Failed to convert {filepath} to PDF. Error: {e}")
            finally:
                wb.Close(False)
                excel.Quit()
    

    # Create the main window
    window = tk.Tk()
    window.title("Excel to PDF Converter")
    window.geometry("800x200")

    # Create the select button
    select_button = tk.Button(window, text="Select .xlsx files to convert to .pdf", font = "Verdana 10 bold", command=select_files)
    select_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    # Create the label to display selected files
    files_label = tk.Label(window, text="", wraplength=700, justify=tk.LEFT)
    files_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Create the reselect button
    reselect_button = tk.Button(window, text="Reselect Files", command=reselect_files)
    reselect_button.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    # Create the convert button
    convert_button = tk.Button(window, text="Convert Files", command=convert_files)
    convert_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)

    # Start the main event loop
    window.mainloop()
