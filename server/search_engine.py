import os
import PyPDF2
import pandas as pd
import re

# Use relative paths as requested 
DOCUMENTS_DIR = "data"

def search_in_txt_html(file_path, keyword, is_regex=False):
    """ Search for a keyword or regex in TXT or HTML files and return line numbers. """
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if is_regex:
                    if re.search(keyword, line):
                        results.append(f"Line {line_num}")
                else:
                    if keyword.lower() in line.lower():
                        results.append(f"Line {line_num}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return results

def search_in_pdf(file_path, keyword, is_regex=False):
    """ Search for a keyword in a PDF and return page numbers. """
    pages_found = []
    try:
        with open(file_path, 'rb') as pdf_file:
            # Updated for PyPDF2 version 3.0+
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text:
                    if is_regex:
                        if re.search(keyword, text):
                            pages_found.append(f"Page {page_num}")
                    elif keyword.lower() in text.lower():
                        pages_found.append(f"Page {page_num}")
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return pages_found

def search_in_excel(file_path, keyword, is_regex=False):
    """ Search in Excel and return Sheet name and Cell location. """
    locations = []
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            for row_idx, row in df.iterrows():
                for col_idx, value in enumerate(row):
                    val_str = str(value)
                    if is_regex:
                        if re.search(keyword, val_str):
                            locations.append(f"Sheet '{sheet_name}', Row {row_idx+2}, Col {col_idx+1}")
                    elif keyword.lower() in val_str.lower():
                        locations.append(f"Sheet '{sheet_name}', Row {row_idx+2}, Col {col_idx+1}")
    except Exception as e:
        print(f"Error reading Excel {file_path}: {e}")
    return locations