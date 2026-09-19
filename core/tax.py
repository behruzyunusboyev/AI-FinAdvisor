from decimal import Decimal, ROUND_HALF_UP
from typing import Literal


TURNOVER_TAX_RATE = Decimal("0.04")
VAT_AND_PROFIT_TAX_RATE = Decimal("0.27")
VAT_PROFIT_REGIME_THRESHOLD = Decimal("1000000000")
CENT = Decimal("0.01")

TaxRegime = Literal["turnover_tax", "vat_plus_profit_tax"]


def estimate_tax(
    annual_turnover: Decimal,
    employee_count: int,
) -> tuple[TaxRegime, Decimal]:
    """Select a tax regime and estimate annual tax from turnover."""
    if annual_turnover < 0:
        raise ValueError("annual_turnover cannot be negative")
    if employee_count < 0:
        raise ValueError("employee_count cannot be negative")

    if annual_turnover < VAT_PROFIT_REGIME_THRESHOLD:
        regime: TaxRegime = "turnover_tax"
        estimated_tax = annual_turnover * TURNOVER_TAX_RATE
    else:
        regime = "vat_plus_profit_tax"
        estimated_tax = annual_turnover * VAT_AND_PROFIT_TAX_RATE

    return regime, estimated_tax.quantize(CENT, rounding=ROUND_HALF_UP)
