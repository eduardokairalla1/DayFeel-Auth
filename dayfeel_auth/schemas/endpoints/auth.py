"""
Payload schemas for auth endpoints.
"""

# --- IMPORTS ---
from pydantic import BaseModel
from pydantic import EmailStr


# --- CODE ---
class LoginPayload(BaseModel):
    """
    Login payload.
    """
    email: EmailStr
    password: str


class RefreshPayload(BaseModel):
    """
    Refresh token payload.
    """
    refresh_token: str
