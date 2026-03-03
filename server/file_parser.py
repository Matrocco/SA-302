import pandas as pd
import PyPDF2
import os

def search_in_pdf(path, keyword):
    """
    Extracts text from each page of a PDF and finds matches.
    Based on course recommendations for PyPDF2.
    """
    matches = []
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text and keyword.lower() in text.lower():
                    matches.append(f"Page {i}")
    except Exception as e:
        return f"Error reading PDF: {e}"
    return ", ".join(matches)

def search_in_excel(path, keyword):
    """
    Searches for a keyword across all cells in an Excel file using pandas.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(path)
        # Check if the keyword exists in any cell (converted to string for safety)
        mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
        matching_indices = df.index[mask].tolist()
        
        if matching_indices:
            # Return line numbers (index + 2 because of header and 0-based index)
            return ", ".join([str(idx + 2) for idx in matching_indices])
    except Exception as e:
        return f"Error reading Excel: {e}"
    return ""