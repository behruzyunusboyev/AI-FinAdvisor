import unittest

from ai.llm_wrapper import AIAnalysisClient


class AIAnalysisClientTests(unittest.TestCase):
    def test_valid_ai_json_matches_the_required_schema(self) -> None:
        result = AIAnalysisClient._validate_text(
            '''{"executive_summary":"Xulosa","swot":{"strengths":["S"],"weaknesses":["W"],"opportunities":["O"],"threats":["T"]},"marketing_strategy":"Reja"}'''
        )
        self.assertEqual(result["executive_summary"], "Xulosa")
        self.assertEqual(result["swot"]["threats"], ["T"])

    def test_invalid_ai_json_is_rejected(self) -> None:
        with self.assertRaises((KeyError, ValueError)):
            AIAnalysisClient._validate_text('{"executive_summary":"Xulosa","swot":"not-a-dictionary"}')

    def test_unavailable_provider_has_safe_uzbek_fallback(self) -> None:
        result = AIAnalysisClient._unavailable_analysis("Qahvaxona")
        self.assertIn("Qahvaxona", result["executive_summary"])
        self.assertIn("strengths", result["swot"])
        self.assertTrue(result["marketing_strategy"])


if __name__ == "__main__":
    unittest.main()
