from html import escape
from typing import Mapping

from pdf.exporter import PdfDocument


REQUIRED_SECTIONS = (
    "executive_summary",
    "swot",
    "marketing_plan",
    "financial_plan",
)


class WeasyPrintBusinessPlanExporter:
    def __init__(self, *, filename: str = "business-plan.pdf") -> None:
        self._filename = filename

    def export(self, business_plan: Mapping[str, str]) -> PdfDocument:
        missing_sections = [
            section for section in REQUIRED_SECTIONS if section not in business_plan
        ]
        if missing_sections:
            raise ValueError(
                f"Business plan is missing sections: {', '.join(missing_sections)}"
            )
        if not all(isinstance(business_plan[section], str) for section in REQUIRED_SECTIONS):
            raise ValueError("Business-plan sections must be strings")

        try:
            from weasyprint import HTML
        except (ImportError, OSError) as error:
            raise RuntimeError(
                "WeasyPrint system libraries are unavailable"
            ) from error

        html = self._render_html(business_plan)
        return PdfDocument(
            content=HTML(string=html).write_pdf(),
            filename=self._filename,
        )

    @staticmethod
    def _render_html(business_plan: Mapping[str, str]) -> str:
        sections = (
            ("Executive Summary", business_plan["executive_summary"]),
            ("SWOT", business_plan["swot"]),
            ("Marketing Plan", business_plan["marketing_plan"]),
            ("Financial Plan", business_plan["financial_plan"]),
        )
        body = "".join(
            f"<section><h2>{escape(title)}</h2><p>{escape(content)}</p></section>"
            for title, content in sections
        )
        return (
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<style>body{font-family:Arial,sans-serif;margin:32px}"
            "section{page-break-inside:avoid}h1{color:#17365d}"
            "h2{color:#24527a}p{white-space:pre-wrap}</style></head>"
            f"<body><h1>AI FinAdvisor Business Plan</h1>{body}</body></html>"
        )
