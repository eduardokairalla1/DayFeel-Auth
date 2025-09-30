"""
Startup and shutdown event handlers.
"""

# --- IMPORTS ---
from dayfeel_auth import routers
from dayfeel_auth.app import container
from dayfeel_auth.app import health
from dayfeel_auth.db.sqlalchemy.repository.auth_sessions import AuthSessionsRepository
from dayfeel_auth.db.sqlalchemy.repository.users import UsersRepository
from dayfeel_auth.db.sqlalchemy.setup.database_engine import create_database_engine
from fastapi import FastAPI


# --- CODE ---
def on_startup(app: FastAPI) -> None:
    """
    Initialize the service on startup.
    """
    # Mount routers
    routers.mount(app)

    # Create database engine
    database_engine = create_database_engine(url=container['config'].POSTGRES_URL)

    # Initialize users repository
    users_repository = UsersRepository(engine=database_engine)

    # Initialize auth sessions reposository
    auth_sessions_reposository = AuthSessionsRepository(engine=database_engine)

    # Update global container
    container.update({
        'users_repository': users_repository,
        'auth_sessions_reposository': auth_sessions_reposository
    })

    # Set app health as OK
    health.status = 'OK'

    # Log service start
    container['logger'].info('Service started')


def on_shutdown(app: FastAPI) -> None:  #pylint: disable=W0613
    """
    Run on service shutdown.
    """
    # Log service shutdown
    container['logger'].info('Service shutdown')
