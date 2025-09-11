"""
Already Exists Error.
"""

# --- IMPORTS ---
from dayfeel_auth.err.dayfeel_autherror import DayfeelAuthError


# --- CODE ---
class AlreadyExistsError(DayfeelAuthError):
    """
    Already Exists Error.
    """
    message = 'Already Exists Error'
