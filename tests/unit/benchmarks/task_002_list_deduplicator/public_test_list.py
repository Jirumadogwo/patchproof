"""Public tests added during recovery; no historical copy existed."""
from workspace.list_utils import remove_duplicates


def test_preserves_order():
    assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_empty():
    assert remove_duplicates([]) == []


def test_unique():
    assert remove_duplicates([3, 1, 2]) == [3, 1, 2]
