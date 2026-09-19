from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from core.loan import calculate_annuity_payment, get_payment_risk_warning

router = APIRouter()


class LoanCalculationRequest(BaseModel):
    principal: Decimal = Field(gt=0)
    term_months: int = Field(gt=0)
    annual_interest_rate: Decimal = Field(ge=0)
    monthly_income: Decimal = Field(gt=0)


class LoanCalculationResponse(BaseModel):
    monthly_payment: Decimal
    total_payment: Decimal
    risk_warning: str | None


@router.post("/loan/calculate", response_model=LoanCalculationResponse)
def calculate_loan(request: LoanCalculationRequest) -> LoanCalculationResponse:
    monthly_payment = calculate_annuity_payment(
        principal=request.principal,
        annual_interest_rate=request.annual_interest_rate,
        term_months=request.term_months,
    )
    return LoanCalculationResponse(
        monthly_payment=monthly_payment,
        total_payment=(monthly_payment * request.term_months).quantize(Decimal("0.01")),
        risk_warning=get_payment_risk_warning(
            monthly_payment=monthly_payment,
            monthly_income=request.monthly_income,
        ),
    )
