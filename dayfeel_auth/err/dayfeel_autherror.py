"""
Base Dayfeel_auth error.
"""

# --- TYPES ---
from typing import Any


# --- GLOBAL ---
DEFAULT_MESSAGE = 'Generic Dayfeel_auth error'


# --- ERROR CLASS ---
class DayfeelAuthError(Exception):
    """
    Base DayfeelAuth error.
    """
    message = DEFAULT_MESSAGE

    def __init__(self, *args: Any) -> None:
        """
        Initialize a Dayfeel_auth error.

        :param *args: Optional additional context or details for the error.

        :returns: None.
        """
        super().__init__(self.message, *args)
