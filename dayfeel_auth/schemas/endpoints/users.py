"""
Payload schemas for user endpoints.
"""

# --- IMPORTS ---
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator

import re


# --- CODE ---
class RegisterPayload(BaseModel):
    """
    Registration payload.
    """
    email: EmailStr
    password: str
    name: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        """
        Validate password.

        :param cls: class reference.
        :param password: user password.

        :returns: validated password.
        """
        # length check.
        if len(password) < 5:
            raise ValueError('Password must be at least 5 characters long!')

        # uppercase.
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter!')

        # lowercase.
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter!')

        # number.
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one number!')

        # special char.
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character!')

        # no spaces.
        if re.search(r'\s', password):
            raise ValueError('Password must not contain spaces!')

        return password
