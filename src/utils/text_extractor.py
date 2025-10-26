"""
Text extraction utilities for PDF and DOCX files.
"""
import fitz  # PyMuPDF
from docx import Document

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_file: File object containing PDF data
        
    Returns:
        str: Extracted text from PDF
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

def extract_text_from_docx(docx_file):
    """
    Extract text from a DOCX file.
    
    Args:
        docx_file: File object containing DOCX data
        
    Returns:
        str: Extracted text from DOCX
    """
    doc = Document(docx_file)
    return "\n".join(p.text for p in doc.paragraphs)