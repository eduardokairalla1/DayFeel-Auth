"""
HTTP routers.
"""

# --- IMPORTS ---
from dayfeel_auth.routers import auth
from dayfeel_auth.routers import system
from dayfeel_auth.routers import users
from fastapi import FastAPI


# --- CODE ---
def mount(app: FastAPI) -> None:
    """
    Mount all routers on application.

    :param app: main app router

    :returns: nothing
    """
    app.include_router(system.router, tags = ['system'])
    app.include_router(users.router, tags = ['users'])
    app.include_router(auth.router, tags = ['auth'], prefix='/auth')
