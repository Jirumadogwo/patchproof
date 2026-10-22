"""
Public tests for task_001_string_reverser.
Visible to candidate agents during evaluation.
"""

from workspace.string_utils import reverse_string


def test_reverse_basic():
    """Test basic word reversal."""
    assert reverse_string("cat") == "tac"
    assert reverse_string("hello") == "olleh"


def test_reverse_empty():
    """Test empty string edge case."""
    assert reverse_string("") == ""


def test_reverse_single_char():
    """Test single character edge case."""
    assert reverse_string("a") == "a"
