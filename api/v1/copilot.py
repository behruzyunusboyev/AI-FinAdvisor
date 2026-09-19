from decimal import Decimal, ROUND_HALF_UP

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import DailyLog, Project

router = APIRouter()


class DailyCheckRequest(BaseModel):
    project_id: str = Field(min_length=1)
    daily_revenue: int = Field(ge=0)
    daily_expense: int = Field(ge=0)


class DailyCheckResponse(BaseModel):
    daily_profit: int
    bep_progress_pct: float
    insight: str


@router.post("/copilot/daily-check", response_model=DailyCheckResponse, status_code=201)
async def daily_check(payload: DailyCheckRequest, session: AsyncSession = Depends(get_session)) -> DailyCheckResponse:
    project = await session.get(Project, payload.project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    daily_profit = payload.daily_revenue - payload.daily_expense
    daily_bep = Decimal(str(project.financial_data["break_even"]["daily_break_even_revenue"]))
    progress = (Decimal(payload.daily_revenue) / daily_bep * Decimal("100")) if daily_bep else Decimal("0")
    progress = progress.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    insight = f"Bugungi sof foyda {daily_profit:,} so'm. Kunlik BEP bajarilishi {progress}%."
    result = {"daily_profit": daily_profit, "bep_progress_pct": float(progress), "insight": insight}
    session.add(DailyLog(project_id=project.id, daily_revenue=payload.daily_revenue, daily_expense=payload.daily_expense, result_data=result))
    await session.commit()
    return DailyCheckResponse(**result)
