import pytesseract
from PIL import Image
import pdfplumber
from docx import Document

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def ingest_document(file_path):
    ext = file_path.lower().split('.')[-1]
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == "docx":
        text = extract_text_from_docx(file_path)
    elif ext in ["png", "jpg", "jpeg"]:
        text = extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    clauses = [f"Clause{clause.strip()}" for clause in text.split("Clause") if clause.strip()]
    return clauses