"""
Global service objects.
"""

# --- IMPORTS ---
from dayfeel_auth.models import Config
from dayfeel_auth.models import Health
from dayfeel_auth.models import Info
from fastapi import FastAPI


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
