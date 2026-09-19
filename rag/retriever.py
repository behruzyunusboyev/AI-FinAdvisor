from dataclasses import dataclass
from typing import Any, Protocol, Sequence


@dataclass(frozen=True)
class RetrievedDocument:
    content: str
    source: str


class TaxKnowledgeRetriever(Protocol):
    """Contract boundary for retrieving Uzbekistan tax guidance."""

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> Sequence[RetrievedDocument]:
        """Return the most relevant tax documents for a query."""


class ChromaTaxKnowledgeRetriever:
    def __init__(self, collection: Any) -> None:
        self._collection = collection

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> Sequence[RetrievedDocument]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        results = self._collection.query(
            query_texts=[query],
            n_results=limit,
        )
        documents = results.get("documents") or [[]]
        metadatas = results.get("metadatas") or [[]]

        return [
            RetrievedDocument(
                content=content,
                source=self._source_from_metadata(metadata),
            )
            for content, metadata in zip(documents[0], metadatas[0])
        ]

    @staticmethod
    def _source_from_metadata(metadata: Any) -> str:
        if isinstance(metadata, dict) and isinstance(metadata.get("source"), str):
            return metadata["source"]
        return "unknown"
