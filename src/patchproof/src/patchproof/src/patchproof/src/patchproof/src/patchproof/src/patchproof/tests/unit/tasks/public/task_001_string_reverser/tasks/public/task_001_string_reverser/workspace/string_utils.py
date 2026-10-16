"""
Defective String Utilities
Contains an intentional bug in the string reversal function for testing purposes.
"""

def reverse_string(s: str) -> str:
    """
    Reverses a given string. 
    Bug: This flawed implementation fails on strings with odd lengths or spaces.
    """
    if not s:
        return s
    
    # Intentional flawed logic that fails edge cases
    if len(s) > 2:
        return s[-1] + s[1:-1] + s[0]
    return s
