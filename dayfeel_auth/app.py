"""
Global service objects.
"""

# --- IMPORTS ---
from dayfeel_auth.models import Config
from dayfeel_auth.models import Health
from dayfeel_auth.models import Info
from dayfeel_auth.schemas.container import Container
from fastapi import FastAPI
from loguru import logger

import sys


# --- CODE ---
# FastAPI app
app = FastAPI(
    title = 'Dayfeel_auth',
    description = 'This is a service to take care of DayFeel API authentications'
)

# Configuration
config = Config()

# Info
info = Info(
    name = app.title,
    description = app.description,
    version = app.version,
    extra = {}
)

# System health
health = Health()

# Initialize logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
           "<level>{level:<8}</level> | "
           "<white>{message}</white>",
    level="DEBUG",
    enqueue=True
)

# Initialize container
container: Container = {
    'config': config,
    'logger': logger
}
