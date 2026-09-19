# Configuration

Copy `.env.example` to `.env` and set environment variables before starting
Uvicorn. Do not commit `.env` or real API keys.

## OpenAI

`OPENAI_API_KEY` is required by
`POST /api/v1/business-plan/generate`. If it is missing, the endpoint returns
HTTP `503`.

## ChromaDB

RAG context is enabled only when both variables are set:

- `CHROMA_PERSIST_DIRECTORY` — path to the persistent ChromaDB directory
- `CHROMA_TAX_COLLECTION` — existing ChromaDB collection name

If either variable is missing, business-plan generation runs without RAG
context.

Example startup:

```bash
set -a
source .env
set +a
uvicorn main:app --reload
```
