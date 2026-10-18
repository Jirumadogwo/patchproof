"""
Unit tests for PatchProof Evaluator
"""

import pytest
from patchproof.evaluator import PatchEvaluator


def test_evaluator_initialization():
    evaluator = PatchEvaluator(timeout=10)
    assert evaluator.timeout == 10
