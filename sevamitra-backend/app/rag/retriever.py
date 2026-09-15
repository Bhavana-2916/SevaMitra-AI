import os

from supabase import create_client
from dotenv import load_dotenv

from app.rag.embeddings import embed_text

load_dotenv()

_supabase = None


def get_supabase_client():
    global _supabase

    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SECRET_KEY")

        if not url or not key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required in .env"
            )

        _supabase = create_client(url, key)

    return _supabase


def retrieve_context(
    question: str,
    top_k: int = 8,
    min_similarity: float = 0.20,
) -> str:
    """
    Search Supabase pgvector for relevant document chunks.

    A lower threshold is used for the first version because short user
    questions do not always produce a cosine similarity above 0.55.
    """

    supabase = get_supabase_client()

    query_vector = embed_text(question)

    result = supabase.rpc(
        "match_document_chunks",
        {
            "query_embedding": query_vector,
            "match_threshold": min_similarity,
            "match_count": top_k,
        },
    ).execute()

    chunks = result.data or []

    print("RAG QUESTION:", question)
    print("RAG MATCHES:", len(chunks))

    if not chunks:
        return ""

    for chunk in chunks:
        print(
            "RAG MATCH:",
            chunk.get("filename"),
            "similarity=",
            chunk.get("similarity"),
        )

    return "\n\n---\n\n".join(
        f"(From {c.get('filename', 'official source')}): {c.get('content', '')}"
        for c in chunks
    )