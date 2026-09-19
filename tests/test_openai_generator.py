import unittest

from ai.openai_generator import OpenAIBusinessPlanGenerator
from rag.retriever import RetrievedDocument


class FakeCompletions:
    def __init__(self, content: str) -> None:
        self.content = content
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        return type(
            "Response",
            (),
            {
                "choices": [
                    type(
                        "Choice",
                        (),
                        {
                            "message": type(
                                "Message",
                                (),
                                {"content": self.content},
                            )()
                        },
                    )()
                ]
            },
        )()


class FakeClient:
    def __init__(self, content: str) -> None:
        self.completions = FakeCompletions(content)
        self.chat = type("Chat", (), {"completions": self.completions})()


class OpenAIGeneratorTests(unittest.TestCase):
    def test_parses_business_plan_sections(self) -> None:
        client = FakeClient(
            '{"executive_summary":"Summary","swot":"SWOT",'
            '"marketing_plan":"Marketing","financial_plan":"Finance"}'
        )
        generator = OpenAIBusinessPlanGenerator(client)

        result = generator.generate({"project_name": "Test"})

        self.assertEqual(result.swot, "SWOT")
        self.assertEqual(client.completions.request["model"], "gpt-4o-mini")
        self.assertEqual(
            client.completions.request["response_format"],
            {"type": "json_object"},
        )

    def test_includes_retrieved_tax_context(self) -> None:
        class FakeRetriever:
            def search(self, query: str, *, limit: int = 5):
                self.query = query
                self.limit = limit
                return [
                    RetrievedDocument(
                        content="QQS bo'yicha qoida",
                        source="tax-law.md",
                    )
                ]

        client = FakeClient(
            '{"executive_summary":"Summary","swot":"SWOT",'
            '"marketing_plan":"Marketing","financial_plan":"Finance"}'
        )
        retriever = FakeRetriever()
        generator = OpenAIBusinessPlanGenerator(client, retriever=retriever)

        generator.generate(
            {
                "industry": "Savdo",
                "description": "Chakana savdo",
                "location": "Toshkent",
            }
        )

        prompt = client.completions.request["messages"][1]["content"]
        self.assertIn("QQS bo'yicha qoida", prompt)
        self.assertEqual(retriever.limit, 3)

    def test_rejects_missing_sections(self) -> None:
        generator = OpenAIBusinessPlanGenerator(
            FakeClient('{"executive_summary":"Summary"}')
        )

        with self.assertRaisesRegex(ValueError, "missing sections"):
            generator.generate({"project_name": "Test"})


if __name__ == "__main__":
    unittest.main()
