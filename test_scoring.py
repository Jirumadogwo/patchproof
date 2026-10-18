"""
Unit tests for PatchProof Score Calculator
"""

import pytest
from patchproof.scoring import ScoreCalculator


def test_pass_rate_calculation():
    assert ScoreCalculator.calculate_pass_rate(5, 10) == 0.5
    assert ScoreCalculator.calculate_pass_rate(10, 10) == 1.0
    assert ScoreCalculator.calculate_pass_rate(0, 0) == 0.0


def test_determine_status():
    assert ScoreCalculator.determine_status(1.0, True) == "SUCCESS"
    assert ScoreCalculator.determine_status(0.5, True) == "REGRESSION"
    assert ScoreCalculator.determine_status(0.0, True) == "TEST_FAILURE"
    assert ScoreCalculator.determine_status(1.0, False) == "ANTI_GAMING_FAILURE"
