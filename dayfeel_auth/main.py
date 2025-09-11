"""
Service entry point.
"""

# --- IMPORTS ---
from contextlib import asynccontextmanager
from dayfeel_auth.app import app
from dayfeel_auth.events import on_shutdown
from dayfeel_auth.events import on_startup
from dayfeel_auth.responders import errors  # pylint: disable=W0611
from fastapi import FastAPI


# --- CODE ---
@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Handles startup and shutdown events for the application.
    """
    # Startup tasks
    on_startup(application)

    # Run the app
    try:
        yield

    # Shutdown tasks
    finally:
        on_shutdown(application)

# Attach lifespan to the app
app.router.lifespan_context = lifespan
