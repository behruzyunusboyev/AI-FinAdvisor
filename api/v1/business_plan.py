from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from ai.llm_wrapper import AIAnalysisClient
from core.financial_engine import build_financials
from database import get_session
from models import Project

router = APIRouter()


class BusinessPlanRequest(BaseModel):
    region: str = Field(min_length=1, max_length=100)
    business_type: str = Field(min_length=1, max_length=120)
    own_capital: int = Field(ge=0)
    need_credit: bool
    requested_loan_amount: int = Field(ge=0)
    loan_term_months: int = Field(ge=1, le=120)
    employees_count: int = Field(ge=0, le=1000)
    average_salary_per_employee: int = Field(ge=0)
    monthly_rent: int = Field(ge=0)
    entity_type: Literal["yatt", "mchj"]

    @model_validator(mode="after")
    def validate_credit_fields(self) -> "BusinessPlanRequest":
        if self.need_credit and self.requested_loan_amount <= 0:
            raise ValueError("requested_loan_amount must be positive when need_credit is true")
        if not self.need_credit and self.requested_loan_amount != 0:
            raise ValueError("requested_loan_amount must be zero when need_credit is false")
        if self.own_capital + self.requested_loan_amount <= 0:
            raise ValueError("at least one financing source must be positive")
        return self


class SWOT(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]


class AIAnalysis(BaseModel):
    executive_summary: str
    swot: SWOT
    marketing_strategy: str


class BusinessPlanResponse(BaseModel):
    financials: dict
    ai_analysis: AIAnalysis
    project_id: str


@router.post("/business-plan/generate", response_model=BusinessPlanResponse, status_code=201)
async def generate_business_plan(request: BusinessPlanRequest, session: AsyncSession = Depends(get_session)) -> BusinessPlanResponse:
    request_data = request.model_dump()
    financial_inputs = {
        key: request_data[key]
        for key in (
            "own_capital", "need_credit", "requested_loan_amount", "loan_term_months",
            "employees_count", "average_salary_per_employee", "monthly_rent", "entity_type",
        )
    }
    financials = build_financials(**financial_inputs)
    analysis = await AIAnalysisClient().analyze(request_data, financials)
    project = Project(region=request.region, business_type=request.business_type, request_data=request_data, financial_data=financials, ai_analysis=analysis)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return BusinessPlanResponse(financials=financials, ai_analysis=AIAnalysis.model_validate(analysis), project_id=project.id)
