"""
User roles.
"""

# --- IMPORTS ---
from enum import Enum


# --- CODE ---
class UserRole(Enum):
    """
    Represents user roles in the system.
    """
    USER = "user"
    ADMIN = "admin"
