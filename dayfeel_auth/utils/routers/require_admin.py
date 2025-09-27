"""
Dependency to restrict FastAPI routes to admin users only.
"""

# --- IMPORTS ---
from dayfeel_auth.utils.auth import decode_token
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer


# --- TYPES ---
from typing import Any
from typing import Dict


# --- GLOBALS ---
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- code ---
def require_admin(token: str = Depends(OAUTH2_SCHEME)) -> Dict[str, Any]:
    """
    Restrict route access to admin users only.

    :param token: JWT access token extracted from the Authorization header.

    :returns: Decoded token payload.

    :raises HTTPException 401: If role is missing.
    :raises HTTPException 403: If user role is not 'admin'.
    """
    # Decoded JWT token
    decoded_token = decode_token(token)

    # Get user role
    role = decoded_token.get("role")

    # User role not exist: raise 'HTTP' Error
    if role is None:
        raise HTTPException(status_code=401, detail="Access token required")

    # User role not is admin: raise 'HTTP' Error
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    # Retrun decoded token
    return decoded_token
