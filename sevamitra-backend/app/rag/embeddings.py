from sentence_transformers import SentenceTransformer

# Loaded once and reused. This model is free, runs on your own computer
# (no API key, no cost), and produces 384-dimensional vectors.
_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(text: str) -> list[float]:
    """Converts a single string into a 384-number vector."""
    model = get_model()
    return model.encode(text).tolist()


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes the output of chunker.chunk_documents() and adds an
    "embedding" field to each chunk dict, ready to insert into Supabase.
    """
    model = get_model()
    texts = [c["chunk"] for c in chunks]
    vectors = model.encode(texts)

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector.tolist()

    return chunks
