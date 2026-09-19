"""
Quality checks for prompts and business-plan outputs.
- run_adversarial_prompts(): sends ambiguous/edge prompts to generator
- detect_hallucination(plan): checks for numeric tokens or % if placeholder not used
- check_language(plan): ensures Uzbek phrases/characters appear
- validate_schema(plan): ensures required keys exist and types look correct
"""
import re
from typing import Dict, Any, List
import json
from generate_business_plan import generate_business_plan

REQUIRED_KEYS = [
    "executive_summary",
    "swot",
    "marketing",
    "financial_plan",
    "notes",
]


def detect_hallucination(plan: Dict[str, Any]) -> List[str]:
    issues = []
    # look for digits or percent signs in text fields where placeholder should be used
    digit_pattern = re.compile(r"\d+|%")
    for key in ["executive_summary", "marketing", "financial_plan", "notes"]:
        val = plan.get(key)
        if isinstance(val, str):
            if digit_pattern.search(val) and "TO_BE_FILLED_BY_FINANCIAL_MODULE" not in val:
                issues.append(f"Numeric/hallucinated value in '{key}': {val[:80]!r}")
    # SWoT lists
    swot = plan.get('swot', {}) or {}
    for area in ['strengths','weaknesses','opportunities','threats']:
        arr = swot.get(area, [])
        for item in arr:
            if digit_pattern.search(item):
                issues.append(f"Numeric/hallucinated value in swot.{area}: {item!r}")
    return issues


def check_language(plan: Dict[str, Any]) -> List[str]:
    issues = []
    # require presence of some Uzbek-specific characters/words
    uzbek_signs = ["o'", "oʻ", "sh", "qqs", "soliq", "Moliyaviy", "foiz"]
    text = json.dumps(plan, ensure_ascii=False).lower()
    if not any(s in text for s in ['qqs', 'soliq', "o'", "oʻ"]):
        issues.append('No Uzbek keywords found in output')
    return issues


def validate_schema(plan: Dict[str, Any]) -> List[str]:
    issues = []
    for key in REQUIRED_KEYS:
        if key not in plan:
            issues.append(f"Missing key: {key}")
    # swot shape
    swot = plan.get('swot')
    if swot is None or not isinstance(swot, dict):
        issues.append('swot missing or not an object')
    else:
        for sub in ['strengths','weaknesses','opportunities','threats']:
            if sub not in swot:
                issues.append(f"swot.{sub} missing")
    return issues


def run_adversarial_prompts():
    # three adversarial inputs
    cases = [
        { 'project_title': "", 'description': "", 'audience': 'bank' },
        { 'project_title': "No info", 'description': "", 'audience': 'bank' },
        { 'project_title': "High risk plan", 'description': "We expect precise numbers.", 'audience': 'bank' }
    ]
    rag = ["QQS stavkasi 12%.", "4% aylanma rejimi haqida yozuv."]

    summary = []
    for i, ui in enumerate(cases, 1):
        plan = generate_business_plan(ui, rag)
        schema_issues = validate_schema(plan)
        hallu = detect_hallucination(plan)
        lang = check_language(plan)
        summary.append({
            'case': i,
            'ui': ui,
            'schema_issues': schema_issues,
            'hallucinations': hallu,
            'language_issues': lang,
            'plan_preview': plan
        })
    return summary


if __name__ == '__main__':
    res = run_adversarial_prompts()
    print(json.dumps(res, ensure_ascii=False, indent=2))
