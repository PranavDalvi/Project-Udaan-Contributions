import re
from docx import Document
import openpyxl
from glob import glob
import os

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []

    for para in doc.paragraphs:
        full_text.append(para.text)

    return '\n'.join(full_text)

def separate_and_save_to_excel(file_path, excel_path):
    text_content = read_docx(file_path)
    text_content = ' '.join(text_content.split())
    separated_lines = re.split('।|॥', text_content)

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Add headers to the Excel file
    sheet['A1'] = 'Original'
    sheet['B1'] = 'Translated'

    for i, line in enumerate(separated_lines, start=2):  # Start from row 2 to leave space for headers
        cleaned_line = line.strip()
        if cleaned_line:  # Check if the line is not empty before appending
            sheet.append([cleaned_line])

    workbook.save(excel_path)

if __name__ == "__main__":
    for docx_file_path in sorted(glob("/home/*.docx")):
        base_name = os.path.basename(docx_file_path)
        file_name, file_extension = os.path.splitext(base_name)
        excel_file_path = f'./outputs/{file_name}.xlsx'
        print(f"\n Processing {file_name}{file_extension}")
        separate_and_save_to_excel(docx_file_path, excel_file_path)
