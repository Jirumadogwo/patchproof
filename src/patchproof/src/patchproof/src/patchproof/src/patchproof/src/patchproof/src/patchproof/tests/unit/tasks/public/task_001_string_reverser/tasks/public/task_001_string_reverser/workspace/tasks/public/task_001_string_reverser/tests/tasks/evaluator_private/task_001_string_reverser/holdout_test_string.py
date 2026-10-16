"""
Holdout evaluation tests for task_001_string_reverser.
Hidden from candidate agents during evaluation.
"""

from workspace.string_utils import reverse_string


def test_reverse_complex_edges():
    """Test complex strings with spaces, symbols, and mixed cases."""
    assert reverse_string("hello world") == "dlrow olleh"
    assert reverse_string("Python 3.10") == ".01 3 nohtyP"


def test_reverse_palindrome():
    """Test palindromes where reversed string equals original string."""
    assert reverse_string("madam") == "madam"
    assert reverse_string("racecar") == "racecar"
