"""Contract tests that do not require a live PostgreSQL service."""

import os
import unittest

from fastapi.testclient import TestClient

# Tests always use an isolated local SQLite database, never a developer's .env.
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./finadvisor-test.db"

from main import app


class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.__exit__(None, None, None)

    def test_v2_routes_are_registered(self) -> None:
        paths = self.client.get("/openapi.json").json()["paths"]
        self.assertIn("/api/v1/business-plan/generate", paths)
        self.assertIn("/api/v1/copilot/daily-check", paths)
        self.assertIn("/api/v1/export/pdf/{project_id}", paths)
        self.assertIn("post", paths["/api/v1/business-plan/generate"])
        self.assertIn("get", paths["/api/v1/export/pdf/{project_id}"])

    def test_generate_validates_credit_request(self) -> None:
        response = self.client.post(
            "/api/v1/business-plan/generate",
            json={
                "region": "Xorazm", "business_type": "Qahvaxona", "own_capital": 0,
                "need_credit": True, "requested_loan_amount": 0, "loan_term_months": 24,
                "employees_count": 3, "average_salary_per_employee": 3_000_000,
                "monthly_rent": 8_000_000, "entity_type": "yatt",
            },
        )
        self.assertEqual(response.status_code, 422)

    def test_sqlite_business_plan_and_daily_copilot_flow(self) -> None:
        response = self.client.post(
            "/api/v1/business-plan/generate",
            json={
                "region": "Xorazm", "business_type": "Qahvaxona", "own_capital": 100_000_000,
                "need_credit": True, "requested_loan_amount": 50_000_000, "loan_term_months": 24,
                "employees_count": 3, "average_salary_per_employee": 3_000_000,
                "monthly_rent": 8_000_000, "entity_type": "yatt",
            },
        )
        self.assertEqual(response.status_code, 201)
        plan = response.json()
        self.assertIn("bank_readiness", plan["financials"])
        self.assertEqual(plan["financials"]["bank_readiness"]["score"], 100)

        daily = self.client.post(
            "/api/v1/copilot/daily-check",
            json={"project_id": plan["project_id"], "daily_revenue": 2_400_000, "daily_expense": 1_700_000},
        )
        self.assertEqual(daily.status_code, 201)
        self.assertEqual(daily.json()["daily_profit"], 700_000)

    def test_pdf_endpoint_returns_pdf_when_weasyprint_dependencies_are_present(self) -> None:
        response = self.client.post(
            "/api/v1/business-plan/generate",
            json={
                "region": "Xorazm", "business_type": "Qahvaxona", "own_capital": 100_000_000,
                "need_credit": False, "requested_loan_amount": 0, "loan_term_months": 24,
                "employees_count": 2, "average_salary_per_employee": 3_000_000,
                "monthly_rent": 7_000_000, "entity_type": "mchj",
            },
        )
        self.assertEqual(response.status_code, 201)
        pdf = self.client.get(f"/api/v1/export/pdf/{response.json()['project_id']}")
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf.headers["content-type"], "application/pdf")
        self.assertTrue(pdf.content.startswith(b"%PDF"))

if __name__ == "__main__":
    unittest.main()
