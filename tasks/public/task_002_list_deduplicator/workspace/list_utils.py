"""
Defective List Utilities
Contains an intentional bug in the deduplication function (destroys order).
"""

from typing import List, Any

def remove_duplicates(items: List[Any]) -> List[Any]:
    """
    Removes duplicates from a list.
    Bug: Using set() destroys the original order of items.
    """
    if not items:
        return []
    
    # Flawed implementation using set() which scrambles order
    return list(set(items))
