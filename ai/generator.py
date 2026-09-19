from dataclasses import dataclass
from typing import Mapping, Protocol


@dataclass(frozen=True)
class BusinessPlanResult:
    executive_summary: str
    swot: str
    marketing_plan: str
    financial_plan: str


class BusinessPlanGenerator(Protocol):
    """Contract boundary for an AI business-plan generator."""

    def generate(
        self,
        project_data: Mapping[str, object],
    ) -> BusinessPlanResult:
        """Generate business-plan sections from validated project data."""
