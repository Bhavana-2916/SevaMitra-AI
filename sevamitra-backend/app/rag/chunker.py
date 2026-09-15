def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Splits a long text into overlapping chunks so each chunk keeps some
    context from the one before it (helps the retriever not cut a fact
    in half between two chunks).

    chunk_size: max characters per chunk
    overlap: how many characters repeat between consecutive chunks
    """
    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Takes the output of document_loader.load_all_documents() and returns
    a flat list of {"filename": ..., "chunk": ..., "chunk_index": ...}
    ready to be embedded.
    """
    all_chunks = []
    for doc in documents:
        pieces = chunk_text(doc["text"])
        for i, piece in enumerate(pieces):
            all_chunks.append(
                {
                    "filename": doc["filename"],
                    "chunk": piece,
                    "chunk_index": i,
                }
            )
    return all_chunks
