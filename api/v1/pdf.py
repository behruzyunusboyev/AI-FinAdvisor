from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.pdf_service import PdfService
from database import get_session
from models import Project

router = APIRouter()


@router.get("/export/pdf/{project_id}", response_class=Response, responses={200: {"content": {"application/pdf": {}}}})
async def export_project_pdf(project_id: str, session: AsyncSession = Depends(get_session)) -> Response:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        content = PdfService().render(project.id, project.request_data, project.financial_data, project.ai_analysis)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return Response(content=content, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="business-plan-{project.id}.pdf"'})
