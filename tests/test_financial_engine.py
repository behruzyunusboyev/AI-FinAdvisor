import unittest

from core.financial_engine import build_financials


class FinancialEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = build_financials(
            own_capital=100_000_000,
            need_credit=True,
            requested_loan_amount=50_000_000,
            loan_term_months=24,
            employees_count=3,
            average_salary_per_employee=3_000_000,
            monthly_rent=8_000_000,
            entity_type="yatt",
        )

    def test_capex_allocates_all_available_capital(self) -> None:
        capex = self.result["capex"]
        self.assertEqual(capex["total_capex"], 150_000_000)
        self.assertEqual(sum(value for key, value in capex.items() if key != "total_capex"), 150_000_000)

    def test_opex_contains_deterministic_salary_and_loan_payment(self) -> None:
        opex = self.result["opex_monthly"]
        self.assertEqual(opex["salaries"], 9_000_000)
        self.assertGreater(opex["loan_payment"], 0)
        self.assertEqual(opex["total_fixed_opex"], sum(opex[key] for key in ("rent", "salaries", "utilities", "loan_payment")))

    def test_bank_score_is_bounded_and_derived_from_three_rules(self) -> None:
        readiness = self.result["bank_readiness"]
        self.assertGreaterEqual(readiness["score"], 0)
        self.assertLessEqual(readiness["score"], 100)
        self.assertEqual(readiness["score"], 100)

    def test_yatt_tax_is_lower_than_mchj_tax_for_same_plan(self) -> None:
        mchj = build_financials(
            own_capital=100_000_000, need_credit=True, requested_loan_amount=50_000_000,
            loan_term_months=24, employees_count=3, average_salary_per_employee=3_000_000,
            monthly_rent=8_000_000, entity_type="mchj",
        )
        self.assertLess(self.result["tax_analysis"]["estimated_monthly_tax"], mchj["tax_analysis"]["estimated_monthly_tax"])


if __name__ == "__main__":
    unittest.main()
