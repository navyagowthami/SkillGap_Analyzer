import os
import io
import PyPDF2
from docx import Document

def is_valid_file_type(filename):
    valid_extensions = ['.txt', '.pdf', '.doc', '.docx']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def extract_text_from_pdf(file_bytes):
    text_parts = []
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    
    return " ".join(text_parts).strip()

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def parse_file(uploaded_file):
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
    
    if filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
        
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
        
    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
        
    if filename.endswith(".doc"):
        raise ValueError("Legacy .doc files are not supported. Please convert to .docx or .pdf first.")
        
    raise ValueError("Unsupported file type. Please upload .txt, .pdf, or .docx files.")
