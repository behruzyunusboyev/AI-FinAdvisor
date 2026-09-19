from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from core.tax import estimate_tax

router = APIRouter()


class TaxEstimateRequest(BaseModel):
    annual_turnover: Decimal = Field(ge=0)
    employee_count: int = Field(ge=0)


class TaxEstimateResponse(BaseModel):
    recommended_tax_regime: str
    estimated_tax: Decimal


@router.post("/tax/estimate", response_model=TaxEstimateResponse)
def estimate_business_tax(request: TaxEstimateRequest) -> TaxEstimateResponse:
    regime, estimated_tax = estimate_tax(
        annual_turnover=request.annual_turnover,
        employee_count=request.employee_count,
    )
    return TaxEstimateResponse(
        recommended_tax_regime=regime,
        estimated_tax=estimated_tax,
    )
