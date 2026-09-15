import os
from pypdf import PdfReader

DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "data", "government_documents")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads a PDF file and returns all its text as one string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def load_all_documents() -> list[dict]:
    """
    Scans data/government_documents/ and returns a list of
    {"filename": ..., "text": ...} for every PDF found there.
    """
    documents = []
    for filename in os.listdir(DOCS_FOLDER):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(DOCS_FOLDER, filename)
            text = extract_text_from_pdf(path)
            documents.append({"filename": filename, "text": text})
    return documents


if __name__ == "__main__":
    # Quick manual test: run `python -m app.rag.document_loader`
    docs = load_all_documents()
    print(f"Loaded {len(docs)} documents:")
    for doc in docs:
        print(f" - {doc['filename']}: {len(doc['text'])} characters")
