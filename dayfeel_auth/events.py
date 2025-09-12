"""
Startup and shutdown event handlers.
"""

# --- IMPORTS ---
from dayfeel_auth import routers
from dayfeel_auth.app import health
from fastapi import FastAPI


# --- CODE ---
def on_startup(app: FastAPI) -> None:
    """
    Initialize the service on startup.
    """
    # Mount routers
    routers.mount(app)

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
