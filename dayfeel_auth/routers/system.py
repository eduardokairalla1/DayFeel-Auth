"""
System endpoints.
"""

# --- IMPORTS ---
from dayfeel_auth.app import health
from dayfeel_auth.app import info
from dayfeel_auth.models import Health
from dayfeel_auth.models import Info
from fastapi import APIRouter
from fastapi.responses import JSONResponse


# --- GLOBAL ---
# Router instance
router = APIRouter()


# --- CODE ---
# Health endpoint
@router.get('/health', response_model = Health)
def get_health() -> JSONResponse:
    """
    Returns the current system health status.
    """
    return JSONResponse(health.dict())


# Info endpoint
@router.get('/info', response_model = Info)
def get_info() -> JSONResponse:
    """
    Returns system information.
    """
    return JSONResponse(info.dict())
