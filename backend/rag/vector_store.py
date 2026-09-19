"""Tekshirilgan RAG bo'laklarini ChromaDB'ga yuklash vositasi."""

import os
from pathlib import Path
from typing import TypedDict


class RagDocument(TypedDict):
    """RAG'ga yuklanadigan, manbasi ko'rsatilgan bitta hujjat bo'lagi."""

    id: str
    text: str
    source_id: str
    source_url: str


def index_documents(
    documents: list[RagDocument],
    persist_directory: str = "backend/rag/chroma_db",
    collection_name: str = "finadvisor_uz",
) -> int:
    """Hujjat bo'laklarini OpenAI embeddinglari bilan ChromaDB'ga saqlaydi.

    Har bir bo'lakning manba identifikatori va URL'i saqlanadi. Shu sababli
    retrieval qilingan fakt keyinchalik rasmiy manba bilan tekshirilishi mumkin.
    """
    if not documents:
        return 0

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable yo'q")

    for document in documents:
        if not all(document.get(field, "").strip() for field in RagDocument.__annotations__):
            raise ValueError("Har bir RAG bo'lagida id, text, source_id va source_url bo'lishi kerak")

    try:
        import chromadb
        from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
    except ImportError as error:
        raise ImportError("chromadb kutubxonasi o'rnatilmagan. Ishga tushiring: pip install chromadb") from error

    embedding_function = OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small",
    )
    client = chromadb.PersistentClient(path=str(Path(persist_directory)))
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},
    )

    collection.upsert(
        ids=[document["id"] for document in documents],
        documents=[document["text"] for document in documents],
        metadatas=[
            {"source_id": document["source_id"], "source_url": document["source_url"]}
            for document in documents
        ],
    )
    return len(documents)
