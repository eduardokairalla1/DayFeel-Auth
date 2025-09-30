"""
Container (dependency injection) Schema.
"""

# --- IMPORTS ---
from dayfeel_auth.db.sqlalchemy.repository.auth_sessions import AuthSessionsRepository
from dayfeel_auth.db.sqlalchemy.repository.users import UsersRepository
from dayfeel_auth.models import Config


# --- TYPES ---
from loguru._logger import Logger
from typing import TypedDict


# --- CODE ---
class Container(TypedDict):
    """
    Structure for global application resources.
    """
    config: Config
    logger: Logger
    users_repository: UsersRepository
    auth_sessions_reposository: AuthSessionsRepository
