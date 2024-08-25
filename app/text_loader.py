import fitz  # PyMuPDF
import os
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text, title, and author from the specified PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No such file: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    
    title, author = extract_title_and_author(text)
    return text, title, author

def extract_title_and_author(text):
    """Attempts to extract the title and author from the beginning of the text."""
    lines = text.splitlines()
    
    # Simple heuristics to detect title and author
    title = None
    author = None
    
    # Assume title might be the first non-empty line
    for line in lines:
        if line.strip():
            title = line.strip()
            break
    
    # Look for the author in the subsequent lines
    author_patterns = ["by ", "BY ", "de ", "DE "]
    for line in lines:
        if any(pattern in line for pattern in author_patterns):
            author = line.strip().replace("by ", "").replace("BY ", "").replace("de ", "").replace("DE ", "")
            break
    
    return title, author
