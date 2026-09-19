"""Deterministic financial calculations for the business-plan contract.

Every monetary output is derived here. AI clients receive completed values only
and are never asked to calculate, estimate, or alter a number.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

MONEY = Decimal("1")
PERCENT = Decimal("0.01")
DEFAULT_ANNUAL_LOAN_RATE = Decimal("24")
DEFAULT_UTILITIES = Decimal("2000000")
GROSS_MARGIN = Decimal("0.60")
AVERAGE_TICKET = Decimal("30000")
PLANNING_REVENUE_MULTIPLIER = Decimal("1.20")


def _money(value: Decimal) -> int:
    return int(value.quantize(MONEY, rounding=ROUND_HALF_UP))


def _percent(value: Decimal) -> float:
    return float(value.quantize(PERCENT, rounding=ROUND_HALF_UP))


def annuity_payment(principal: Decimal, months: int, annual_rate: Decimal = DEFAULT_ANNUAL_LOAN_RATE) -> Decimal:
    if principal <= 0 or months <= 0:
        return Decimal("0")
    monthly_rate = annual_rate / Decimal("1200")
    factor = (Decimal("1") + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - Decimal("1"))


def build_financials(
    *, own_capital: int, need_credit: bool, requested_loan_amount: int,
    loan_term_months: int, employees_count: int,
    average_salary_per_employee: int, monthly_rent: int, entity_type: str,
) -> dict:
    """Return the full financial response using reproducible, documented rules."""
    own = Decimal(own_capital)
    loan = Decimal(requested_loan_amount if need_credit else 0)
    available_capital = own + loan
    allocation = {
        "equipment": Decimal("0.45"), "renovation": Decimal("0.20"),
        "furniture": Decimal("0.10"), "initial_stock": Decimal("0.10"),
        "marketing": Decimal("0.05"), "emergency_reserve": Decimal("0.10"),
    }
    capex = {key: _money(available_capital * share) for key, share in allocation.items()}
    capex["total_capex"] = _money(available_capital)

    salaries = Decimal(employees_count * average_salary_per_employee)
    loan_payment = annuity_payment(loan, loan_term_months) if loan else Decimal("0")
    fixed_opex = Decimal(monthly_rent) + salaries + DEFAULT_UTILITIES + loan_payment
    opex = {
        "rent": monthly_rent, "salaries": _money(salaries), "utilities": _money(DEFAULT_UTILITIES),
        "loan_payment": _money(loan_payment), "total_fixed_opex": _money(fixed_opex),
    }

    monthly_bep = fixed_opex / GROSS_MARGIN
    daily_bep = monthly_bep / Decimal("30")
    customers = (daily_bep / AVERAGE_TICKET).to_integral_value(rounding=ROUND_HALF_UP)
    break_even = {
        "monthly_break_even_revenue": _money(monthly_bep),
        "daily_break_even_revenue": _money(daily_bep),
        "required_daily_customers": int(customers),
    }

    planning_revenue = monthly_bep * PLANNING_REVENUE_MULTIPLIER
    rate = Decimal("0.01") if entity_type == "yatt" else Decimal("0.04")
    regime = "1% aylanma solig'i (YaTT 2026)" if entity_type == "yatt" else "4% aylanma solig'i (MCHJ 2026)"
    tax = {
        "selected_regime": regime,
        "estimated_monthly_tax": _money(planning_revenue * rate),
        "alternative_regimes": {
            "yatt_1_percent": _money(planning_revenue * Decimal("0.01")),
            "mchj_4_percent": _money(planning_revenue * Decimal("0.04")),
            "vat_12_percent": _money(planning_revenue * Decimal("0.12")),
        },
    }

    own_share = (own / available_capital * Decimal("100")) if available_capital else Decimal("0")
    dsti = (loan_payment / planning_revenue * Decimal("100")) if planning_revenue else Decimal("100")
    safety_margin = (planning_revenue - monthly_bep) / planning_revenue * Decimal("100") if planning_revenue else Decimal("0")
    score = (35 if own_share >= 30 else 0) + (35 if dsti < 40 else 0) + (30 if safety_margin >= 10 else 0)
    status = "Yuqori ehtimol" if score >= 70 else "O'rta ehtimol" if score >= 35 else "Past ehtimol"
    bank_readiness = {
        "score": score, "status": status, "debt_service_ratio": _percent(dsti),
        "own_capital_share_pct": _percent(own_share), "bep_safety_margin_pct": _percent(safety_margin),
        "recommendation": f"O'z mablag'ingiz ulushi {_percent(own_share)}%, DSTI {_percent(dsti)}%. Bank bahosi: {status}.",
    }
    return {"capex": capex, "opex_monthly": opex, "break_even": break_even, "tax_analysis": tax, "bank_readiness": bank_readiness, "assumptions": {"annual_loan_rate_pct": float(DEFAULT_ANNUAL_LOAN_RATE), "gross_margin_pct": float(GROSS_MARGIN * 100), "average_ticket": _money(AVERAGE_TICKET), "planning_revenue_multiplier": float(PLANNING_REVENUE_MULTIPLIER)}}
