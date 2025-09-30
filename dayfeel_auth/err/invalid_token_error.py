"""
Invalid Token Error.
"""

# --- IMPORTS ---
from dayfeel_auth.err.dayfeel_autherror import DayfeelAuthError


# --- CODE ---
class InvalidTokenError(DayfeelAuthError):
    """
    Invalid Token Error.
    """
    message = 'Invalid Token Error'
