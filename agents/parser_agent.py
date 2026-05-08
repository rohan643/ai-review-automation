"""Agent 1: Document Parser — extracts structured data from PDFs and DOCX files."""
import pdfplumber, json
from pathlib import Path


def parse_document(path: str) -> dict:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(path)
    elif suffix in (".docx", ".doc"):
        return _parse_docx(path)
    raise ValueError(f"Unsupported format: {suffix}")


def _parse_pdf(path: str) -> dict:
    text_blocks = []
    tables = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_blocks.append(page.extract_text() or "")
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return {
        "type": "pdf",
        "page_count": len(text_blocks),
        "full_text": "\n".join(text_blocks),
        "tables": tables,
        "metadata": {}
    }


def _parse_docx(path: str) -> dict:
    from docx import Document
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return {
        "type": "docx",
        "full_text": "\n".join(paragraphs),
        "tables": [],
        "metadata": {}
    }
