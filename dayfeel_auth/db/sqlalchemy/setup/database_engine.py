"""
Database engine factory.
"""

# --- IMPORTS ---
from sqlalchemy import create_engine


# --- TYPES ---
from sqlalchemy import Engine


# -- CODE ---
def create_database_engine(url: str) -> Engine:
    """
    Creates the SQLAlchemy engine used for database connections.

    :param url: Database connection string.

    :returns: Configured Engine instance.
    """
    engine = create_engine(url=url, echo=False, future=True)

    return engine
