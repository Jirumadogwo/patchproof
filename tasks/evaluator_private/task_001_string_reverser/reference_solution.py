"""
Reference Solution for task_001_string_reverser.
Represents the correct implementation that resolves the bug and passes all tests.
"""

def reverse_string(s: str) -> str:
    """
    Correctly reverses a given string using Python slicing.
    """
    if not s:
        return s
    
    return s[::-1]
