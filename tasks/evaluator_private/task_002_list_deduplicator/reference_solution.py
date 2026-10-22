"""
Reference Solution for task_002_list_deduplicator.
Correctly removes duplicates while preserving original item order.
"""

from typing import List, Any

def remove_duplicates(items: List[Any]) -> List[Any]:
    """
    Removes duplicates from a list while preserving order using dict.fromkeys().
    """
    if not items:
        return []
    
    return list(dict.fromkeys(items))
