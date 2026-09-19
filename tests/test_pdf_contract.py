import unittest
from typing import Mapping

from pdf.exporter import BusinessPlanPdfExporter, PdfDocument
from pdf.weasyprint_exporter import WeasyPrintBusinessPlanExporter

try:
    from weasyprint import HTML
except (ImportError, OSError):
    HTML = None


class StubBusinessPlanPdfExporter:
    def export(self, business_plan: Mapping[str, str]) -> PdfDocument:
        return PdfDocument(
            content=business_plan["executive_summary"].encode(),
            filename="business-plan.pdf",
        )


class PdfContractTests(unittest.TestCase):
    def test_exporter_adapter_returns_pdf_document(self) -> None:
        exporter: BusinessPlanPdfExporter = StubBusinessPlanPdfExporter()
        document = exporter.export({"executive_summary": "Summary"})

        self.assertEqual(document.content, b"Summary")
        self.assertEqual(document.filename, "business-plan.pdf")
        self.assertEqual(document.media_type, "application/pdf")

    @unittest.skipUnless(HTML is not None, "WeasyPrint system libraries unavailable")
    def test_weasyprint_exporter_returns_pdf_bytes(self) -> None:
        exporter = WeasyPrintBusinessPlanExporter()

        document = exporter.export(
            {
                "executive_summary": "Summary",
                "swot": "SWOT",
                "marketing_plan": "Marketing",
                "financial_plan": "Finance",
            }
        )

        self.assertEqual(document.filename, "business-plan.pdf")
        self.assertEqual(document.media_type, "application/pdf")
        self.assertTrue(document.content.startswith(b"%PDF"))

    def test_weasyprint_exporter_rejects_missing_section(self) -> None:
        exporter = WeasyPrintBusinessPlanExporter()

        with self.assertRaisesRegex(ValueError, "missing sections"):
            exporter.export({"executive_summary": "Summary"})


if __name__ == "__main__":
    unittest.main()
