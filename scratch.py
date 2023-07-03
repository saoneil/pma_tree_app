import os
import win32com.client as win32

def convert_excel_to_pdf(filepath):
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False
    excel.DisplayAlerts = False

    wb = excel.Workbooks.Open(filepath)
    output_filepath = os.path.splitext(filepath)[0] + ".pdf"

    try:
        wb.ExportAsFixedFormat(0, output_filepath)
        print(f"Converted {filepath} to PDF successfully!")
    except Exception as e:
        print(f"Failed to convert {filepath} to PDF. Error: {e}")
    finally:
        wb.Close(False)
        excel.Quit()

# Example usage
xlsx_filepath = r"C:\Users\saone\Documents\Python Stuff\pma_tree_app\trees_xlsx\test_tree.xlsx"
print(xlsx_filepath)
# convert_excel_to_pdf(xlsx_filepath)
