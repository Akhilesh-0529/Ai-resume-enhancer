"""Text extraction utilities for PDF and DOCX files."""
import fitz
from docx import Document

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join(p.text for p in doc.paragraphs)