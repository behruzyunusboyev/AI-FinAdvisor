import unittest
from typing import Mapping

from ai.generator import BusinessPlanGenerator, BusinessPlanResult


class StubBusinessPlanGenerator:
    def generate(self, project_data: Mapping[str, object]) -> BusinessPlanResult:
        return BusinessPlanResult(
            executive_summary=str(project_data["project_name"]),
            swot="SWOT",
            marketing_plan="Marketing",
            financial_plan="Finance",
        )


class AiContractTests(unittest.TestCase):
    def test_generator_adapter_returns_contract_sections(self) -> None:
        generator: BusinessPlanGenerator = StubBusinessPlanGenerator()
        result = generator.generate({"project_name": "Test project"})

        self.assertEqual(result.executive_summary, "Test project")
        self.assertEqual(result.swot, "SWOT")
        self.assertEqual(result.marketing_plan, "Marketing")
        self.assertEqual(result.financial_plan, "Finance")


if __name__ == "__main__":
    unittest.main()
