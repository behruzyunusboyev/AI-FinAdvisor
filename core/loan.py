from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def calculate_annuity_payment(
    principal: Decimal,
    annual_interest_rate: Decimal,
    term_months: int,
) -> Decimal:
    """Calculate a fixed monthly annuity payment."""
    if principal <= 0:
        raise ValueError("principal must be greater than zero")
    if annual_interest_rate < 0:
        raise ValueError("annual_interest_rate cannot be negative")
    if term_months <= 0:
        raise ValueError("term_months must be greater than zero")

    monthly_rate = annual_interest_rate / Decimal("1200")
    if monthly_rate == 0:
        payment = principal / Decimal(term_months)
    else:
        factor = (Decimal("1") + monthly_rate) ** term_months
        payment = principal * monthly_rate * factor / (factor - Decimal("1"))

    return payment.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_differential_payments(
    principal: Decimal,
    annual_interest_rate: Decimal,
    term_months: int,
) -> list[Decimal]:
    """Calculate monthly payments with a fixed principal installment."""
    if principal <= 0:
        raise ValueError("principal must be greater than zero")
    if annual_interest_rate < 0:
        raise ValueError("annual_interest_rate cannot be negative")
    if term_months <= 0:
        raise ValueError("term_months must be greater than zero")

    monthly_rate = annual_interest_rate / Decimal("1200")
    principal_installment = principal / Decimal(term_months)
    payments: list[Decimal] = []

    for month in range(term_months):
        remaining_principal = principal - principal_installment * month
        payment = principal_installment + remaining_principal * monthly_rate
        payments.append(payment.quantize(CENT, rounding=ROUND_HALF_UP))

    return payments


def get_payment_risk_warning(
    monthly_payment: Decimal,
    monthly_income: Decimal,
) -> str | None:
    """Return a warning when the monthly payment exceeds half of income."""
    if monthly_payment < 0:
        raise ValueError("monthly_payment cannot be negative")
    if monthly_income <= 0:
        raise ValueError("monthly_income must be greater than zero")

    if monthly_payment / monthly_income > Decimal("0.50"):
        return "To'lov/daromad nisbati 50% dan oshdi"
    return None
