"""
PatchProof Scoring and Result Classification
Classifies evaluation results and calculates deterministic scores.
"""

from enum import Enum
from typing import Dict, Any

class ResultStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    REGRESSION = "REGRESSION"
    INVALID_PATCH = "INVALID_PATCH"
    TEST_FAILURE = "TEST_FAILURE"
    TIMEOUT = "TIMEOUT"
    INFRASTRUCTURE_FAILURE = "INFRASTRUCTURE_FAILURE"
    INCONCLUSIVE = "INCONCLUSIVE"


class ResultClassifier:
    """Classifies evaluation outcomes based on test execution results."""

    @staticmethod
    def classify(public_passed: bool, holdout_passed: bool, regression_passed: bool, execution_error: bool = False) -> ResultStatus:
        """Determines the final status of a candidate patch evaluation."""
        if execution_error:
            return ResultStatus.INFRASTRUCTURE_FAILURE

        if not regression_passed:
            return ResultStatus.REGRESSION

        if public_passed and holdout_passed:
            return ResultStatus.SUCCESS
        elif public_passed and not holdout_passed:
            return ResultStatus.PARTIAL
        else:
            return ResultStatus.TEST_FAILURE

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
