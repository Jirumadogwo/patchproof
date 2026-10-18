"""
PatchProof Scoring & Metrics Calculator
"""

class ScoreCalculator:
    @staticmethod
    def calculate_pass_rate(tests_passed: int, tests_total: int) -> float:
        if tests_total == 0:
            return 0.0
        return round(tests_passed / tests_total, 2)

    @staticmethod
    def determine_status(pass_rate: float, anti_gaming_compliant: bool) -> str:
        if not anti_gaming_compliant:
            return "ANTI_GAMING_FAILURE"
        if pass_rate == 1.0:
            return "SUCCESS"
        if pass_rate > 0.0:
            return "REGRESSION"
        return "TEST_FAILURE"
