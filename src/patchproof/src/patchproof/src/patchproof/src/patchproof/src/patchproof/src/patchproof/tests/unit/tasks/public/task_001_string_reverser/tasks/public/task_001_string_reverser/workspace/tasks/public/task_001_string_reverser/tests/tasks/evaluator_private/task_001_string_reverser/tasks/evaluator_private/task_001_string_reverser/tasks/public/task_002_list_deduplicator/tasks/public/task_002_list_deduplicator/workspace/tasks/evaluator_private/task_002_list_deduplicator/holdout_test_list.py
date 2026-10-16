"""
Holdout evaluation tests for task_002_list_deduplicator.
Hidden from candidate agents during evaluation.
"""

from workspace.list_utils import remove_duplicates


def test_remove_duplicates_mixed_types():
    """Test lists containing mixed data types (integers, strings, floats)."""
    assert remove_duplicates([1, "apple", 1, 2.5, "apple"]) == [1, "apple", 2.5]


def test_remove_duplicates_all_same():
    """Test a list where all elements are identical."""
    assert remove_duplicates([5, 5, 5, 5]) == [5]
