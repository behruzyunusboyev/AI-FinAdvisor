import unittest
from decimal import Decimal

from core.loan import (
    calculate_annuity_payment,
    calculate_differential_payments,
    get_payment_risk_warning,
)
from core.tax import estimate_tax


class LoanCalculationTests(unittest.TestCase):
    def test_annuity_payment(self) -> None:
        self.assertEqual(
            calculate_annuity_payment(Decimal("100000000"), Decimal("24"), 24),
            Decimal("5287109.73"),
        )

    def test_differential_payments_decrease(self) -> None:
        payments = calculate_differential_payments(
            Decimal("1000"),
            Decimal("12"),
            12,
        )

        self.assertEqual(len(payments), 12)
        self.assertEqual(payments[0], Decimal("93.33"))
        self.assertEqual(payments[-1], Decimal("84.17"))
        self.assertGreater(payments[0], payments[-1])

    def test_risk_warning_threshold(self) -> None:
        income = Decimal("1000")

        self.assertIsNone(get_payment_risk_warning(Decimal("500"), income))
        self.assertEqual(
            get_payment_risk_warning(Decimal("501"), income),
            "To'lov/daromad nisbati 50% dan oshdi",
        )


class TaxCalculationTests(unittest.TestCase):
    def test_turnover_tax_regime(self) -> None:
        self.assertEqual(
            estimate_tax(Decimal("500000000"), 5),
            ("turnover_tax", Decimal("20000000.00")),
        )

    def test_vat_and_profit_tax_regime(self) -> None:
        self.assertEqual(
            estimate_tax(Decimal("1000000000"), 0),
            ("vat_plus_profit_tax", Decimal("270000000.00")),
        )


if __name__ == "__main__":
    unittest.main()
