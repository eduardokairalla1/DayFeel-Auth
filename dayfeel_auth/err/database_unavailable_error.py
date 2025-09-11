"""
Database Unavailable Error.
"""

# --- IMPORTS ---
from dayfeel_auth.err.dayfeel_autherror import DayfeelAuthError


# --- CODE ---
class DatabaseUnavailableError(DayfeelAuthError):
    """
    Database Unavailable Error.
    """
    message = 'Database Unavailable Error'
