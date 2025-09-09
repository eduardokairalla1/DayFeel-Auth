"""
Container (dependency injection) Schema.
"""

# --- IMPORTS ---
from dayfeel_auth.models import Config


# --- TYPES ---
from typing import TypedDict


# --- CODE ---
class Container(TypedDict):
    """
    Structure for global application resources.
    """
    config: Config
