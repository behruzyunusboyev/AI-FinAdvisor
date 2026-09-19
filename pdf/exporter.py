from dataclasses import dataclass
from typing import Mapping, Protocol


@dataclass(frozen=True)
class PdfDocument:
    content: bytes
    filename: str
    media_type: str = "application/pdf"


class BusinessPlanPdfExporter(Protocol):
    """Contract boundary for rendering a business plan as a PDF."""

    def export(
        self,
        business_plan: Mapping[str, str],
    ) -> PdfDocument:
        """Render validated business-plan sections as a PDF document."""
