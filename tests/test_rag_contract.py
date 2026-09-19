import unittest
from typing import Sequence

from rag.retriever import (
    ChromaTaxKnowledgeRetriever,
    RetrievedDocument,
    TaxKnowledgeRetriever,
)


class StubTaxKnowledgeRetriever:
    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> Sequence[RetrievedDocument]:
        return [
            RetrievedDocument(
                content=f"Guidance for {query}",
                source="test-source",
            )
        ][:limit]


class RagContractTests(unittest.TestCase):
    def test_retriever_adapter_returns_documents(self) -> None:
        retriever: TaxKnowledgeRetriever = StubTaxKnowledgeRetriever()
        documents = retriever.search("turnover tax", limit=1)

        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].source, "test-source")
        self.assertIn("turnover tax", documents[0].content)

    def test_chroma_retriever_maps_collection_results(self) -> None:
        class FakeCollection:
            def query(self, **kwargs):
                self.kwargs = kwargs
                return {
                    "documents": [["4% turnover tax"]],
                    "metadatas": [[{"source": "tax-law.md"}]],
                }

        collection = FakeCollection()
        retriever = ChromaTaxKnowledgeRetriever(collection)

        documents = retriever.search("turnover tax", limit=1)

        self.assertEqual(documents[0].content, "4% turnover tax")
        self.assertEqual(documents[0].source, "tax-law.md")
        self.assertEqual(collection.kwargs["n_results"], 1)

    def test_chroma_retriever_rejects_invalid_query(self) -> None:
        class FakeCollection:
            def query(self, **kwargs):
                return {}

        retriever = ChromaTaxKnowledgeRetriever(FakeCollection())

        with self.assertRaises(ValueError):
            retriever.search(" ", limit=1)
        with self.assertRaises(ValueError):
            retriever.search("tax", limit=0)


if __name__ == "__main__":
    unittest.main()
