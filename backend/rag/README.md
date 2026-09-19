RAG module — ingest skeleton

Purpose:
- Collect reliable tax/bank/legal source texts (official PDFs -> txt)
- Chunk texts into manageable pieces
- (Later) Embed chunks and load into ChromaDB or other vector DB

Notes and precautions:
- Do not attempt to install chromadb on Windows without build tools; prefer using a Linux dev container or remote server.
- Verify all source texts vs official government sites before ingesting.

Commands:
- Quick smoke test:
  cd backend/rag
  python ingest.py

Files:
- `ingest.py` — chunking and IO helpers
- `sample_chunks.json` — written by the smoke test
