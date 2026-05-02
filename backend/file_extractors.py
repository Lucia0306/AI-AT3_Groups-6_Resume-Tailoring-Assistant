import os
import pdfplumber
from docx import Document


def extract_text_from_pdf(path: str) -> str:
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            texts.append(page_text)
    return "\n".join(texts).strip()


def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    texts = [p.text for p in doc.paragraphs]
    return "\n".join(texts).strip()


def extract_resume_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
