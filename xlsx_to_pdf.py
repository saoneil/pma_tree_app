import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import win32com.client as win32

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

            source_file_name_with_extension = os.path.basename(filepath)
            source_file_name, _ = os.path.splitext(source_file_name_with_extension)
            target_file_name = target_folder + "/" + source_file_name + ".pdf"

            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False

            print(filepath)
            print(target_file_name)
            print("----")

            wb = excel.Workbooks.Open(filepath)
            ws = wb.Worksheets[0]

            #Export worksheet as PDF
            ws.ExportAsFixedFormat(0, target_file_name)

            wb.Close()
            excel.Quit()

    # Create the main window
    window = tk.Tk()
    window.title("Excel to PDF Converter")
    window.geometry("500x200")

    # Create the select button
    select_button = tk.Button(window, text="Select .xlsx files to convert to .pdf", font = "Verdana 10 bold", command=select_files)
    select_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    # Create the label to display selected files
    files_label = tk.Label(window, text="", wraplength=400, justify=tk.LEFT)
    files_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Create the reselect button
    reselect_button = tk.Button(window, text="Reselect Files", command=reselect_files)
    reselect_button.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    # Create the convert button
    convert_button = tk.Button(window, text="Convert Files", command=convert_files)
    convert_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)

    # Start the main event loop
    window.mainloop()
