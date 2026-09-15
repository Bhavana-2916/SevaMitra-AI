# RAG module (not yet built)

This is where the real retrieval pipeline will go, once you're ready to
move past the placeholder KNOWLEDGE_BASE in app/routes/chat.py:

- document_loader.py  -> read PDFs from data/government_documents/
- chunker.py           -> split extracted text into chunks
- embeddings.py         -> turn chunks into vector embeddings
- retriever.py          -> given a user question, fetch the most relevant chunks

For now, chat.py returns answers from a small hardcoded dictionary so the
frontend <-> backend connection can be tested end-to-end first.
