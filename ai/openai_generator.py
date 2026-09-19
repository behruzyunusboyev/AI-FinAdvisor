import json
import os
from typing import Any, Mapping

from openai import OpenAI

from ai.generator import BusinessPlanResult
from rag.retriever import RetrievedDocument, TaxKnowledgeRetriever


SYSTEM_PROMPT = (
    "Siz O'zbekiston biznes va soliq muhitiga ixtisoslashgan moliyaviy "
    "maslahatchisiz. Barcha javoblarni o'zbek tilida yozing."
)
REQUIRED_SECTIONS = (
    "executive_summary",
    "swot",
    "marketing_plan",
    "financial_plan",
)


class OpenAIBusinessPlanGenerator:
    def __init__(
        self,
        client: OpenAI | None = None,
        *,
        model: str = "gpt-4o-mini",
        retriever: TaxKnowledgeRetriever | None = None,
    ) -> None:
        self._client = client or OpenAI(
            api_key=os.environ.get("PLATFORM_OPENAI_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        self._model = model
        self._retriever = retriever

    def generate(self, project_data: Mapping[str, object]) -> BusinessPlanResult:
        context = self._build_tax_context(project_data)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Quyidagi loyiha ma'lumotlari asosida biznes-reja "
                        "bo'limlarini JSON formatida yarating."
                        f"{context}\n"
                        f"{json.dumps(project_data, ensure_ascii=False, default=str)}"
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty business-plan response")

        try:
            sections: Any = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError("OpenAI returned invalid business-plan JSON") from error

        if not isinstance(sections, dict):
            raise ValueError("OpenAI business-plan response must be a JSON object")

        missing_sections = [
            section for section in REQUIRED_SECTIONS if section not in sections
        ]
        if missing_sections:
            raise ValueError(
                f"OpenAI response is missing sections: {', '.join(missing_sections)}"
            )
        if not all(isinstance(sections[section], str) for section in REQUIRED_SECTIONS):
            raise ValueError("OpenAI business-plan sections must be strings")

        return BusinessPlanResult(
            executive_summary=sections["executive_summary"],
            swot=sections["swot"],
            marketing_plan=sections["marketing_plan"],
            financial_plan=sections["financial_plan"],
        )

    def _build_tax_context(self, project_data: Mapping[str, object]) -> str:
        if self._retriever is None:
            return "\n"

        query = " ".join(
            str(project_data.get(field, ""))
            for field in ("industry", "description", "location")
        ).strip()
        if not query:
            return "\n"

        documents = self._retriever.search(query, limit=3)
        if not documents:
            return "\n"

        context = "\n".join(
            self._format_document(document) for document in documents
        )
        return f"\nSoliq bo'yicha kontekst:\n{context}\n"

    @staticmethod
    def _format_document(document: RetrievedDocument) -> str:
        return f"[Manba: {document.source}]\n{document.content}"
