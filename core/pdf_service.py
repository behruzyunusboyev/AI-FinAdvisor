"""Three-page Jinja2 and WeasyPrint report generation."""

import base64
import os
from io import BytesIO
from pathlib import Path

import qrcode
from jinja2 import Environment, FileSystemLoader, select_autoescape


class PdfService:
    def __init__(self) -> None:
        self._templates = Environment(loader=FileSystemLoader(Path(__file__).parent.parent / "templates"), autoescape=select_autoescape(["html", "xml"]))

    def render(self, project_id: str, request: dict, financials: dict, ai_analysis: dict) -> bytes:
        # WeasyPrint's documented Windows lookup path for MSYS2 UCRT64 Pango DLLs.
        msys_dll_directory = Path(r"C:\msys64\ucrt64\bin")
        if os.name == "nt" and msys_dll_directory.is_dir():
            os.environ.setdefault("WEASYPRINT_DLL_DIRECTORIES", str(msys_dll_directory))
        try:
            from weasyprint import HTML
        except (ImportError, OSError) as error:
            raise RuntimeError("WeasyPrint system libraries are unavailable") from error
        planning_revenue = financials["break_even"]["monthly_break_even_revenue"] * financials["assumptions"]["planning_revenue_multiplier"]
        opex = financials["opex_monthly"]["total_fixed_opex"]
        cashflow = [{"month": month, "revenue": planning_revenue, "opex": opex, "net": planning_revenue - opex} for month in range(1, 13)]
        qr = qrcode.make(f"finadvisor://project/{project_id}")
        image = BytesIO(); qr.save(image, format="PNG")
        qr_data_uri = "data:image/png;base64," + base64.b64encode(image.getvalue()).decode("ascii")
        html = self._templates.get_template("report.html").render(project=request, project_id=project_id, financials=financials, ai_analysis=ai_analysis, cashflow=cashflow, qr_data_uri=qr_data_uri)
        return HTML(string=html).write_pdf()
