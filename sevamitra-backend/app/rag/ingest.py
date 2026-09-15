import os
from supabase import create_client
from dotenv import load_dotenv

from app.rag.document_loader import load_all_documents
from app.rag.chunker import chunk_documents
from app.rag.embeddings import embed_chunks
from app.rag.knowledge_base import manual_documents

load_dotenv()


def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    return create_client(url, key)


def ingest():
    """
    Run this once (and again whenever you add new PDFs):
        python -m app.rag.ingest

    It reads every PDF in data/government_documents/, splits it into
    chunks, embeds each chunk, and uploads everything to Supabase.
    """
    print("Loading PDFs...")
    # Curated entries and official PDFs share the same ingestion path. This
    # means adding a verified entry improves both exact fallback and RAG.
    documents = load_all_documents() + manual_documents()
    print(f"Found {len(documents)} PDF(s).")

    print("Splitting into chunks...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings (this runs locally, may take a moment)...")
    chunks = embed_chunks(chunks)

    print("Uploading to Supabase...")
    supabase = get_supabase_client()

    rows = [
        {
            "filename": c["filename"],
            "chunk_index": c["chunk_index"],
            "content": c["chunk"],
            "embedding": c["embedding"],
        }
        for c in chunks
    ]

    # Upload in batches of 50 to avoid oversized requests
    batch_size = 50
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        supabase.table("document_chunks").insert(batch).execute()
        print(f"Uploaded {i + len(batch)} / {len(rows)} chunks")

    print("Done! Your PDFs are now searchable.")


if __name__ == "__main__":
    ingest()
