"""
JWT utility module.
"""

# --- IMPORTS ---
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dayfeel_auth.app import container
from dayfeel_auth.err.invalid_token_error import InvalidTokenError
from uuid import uuid4

import jwt


# --- TYPES ---
from typing import Any
from typing import Dict


# --- GLOBALS ---
SECRET_KEY = container['config'].JWT_SECRET_KEY
ACCESS_TOKEN_EXP_MIN = container['config'].JWT_ACCESS_TOKEN_EXP_MIN
REFRESH_TOKEN_EXP_MIN = container['config'].JWT_REFRESH_TOKEN_EXP_MIN

ISSUER = 'dayfeel-auth'
ALGORITHM = 'HS256'


# --- CODE ---
def generate_access_token(user_id: int, email: str, name: str, role: str) -> Dict[str, Any]:
    """
    Generate a JWT access token.

    :param user_id: Unique identifier of the user.
    :param email: User's email address.
    :param name: User's name.
    :param role: User's role.
    
    :returns: Dict with the encoded token and associated claims.
    """

    # Get the current UTC time
    now = datetime.now(timezone.utc)

    # Access token expiration time
    exp = now + timedelta(minutes=ACCESS_TOKEN_EXP_MIN)

    # Build claims
    claims = {
        'iss': ISSUER,
        'sub': str(user_id),
        'exp': exp,
        'iat': now,
        'nbf': now,
        'jti': str(uuid4()),
        'name': name,
        'email': email,
        'role': role,
    }

    # Generate token
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

    # Log success
    container['logger'].info(f'Generated access token for user_id={user_id}')

    # Return payload
    return {'token': token, 'claims': claims}


def generate_refresh_token(user_id: int) -> Dict[str, Any]:
    """
    Generate a signed JWT used only for refreshing access tokens.

    :param user_id: Unique identifier of the user.
    
    :returns: Dict with the encoded token and associated claims.
    """

    # Get the current UTC time
    now = datetime.now(timezone.utc)

    # Refresh token expiration time
    exp = now + timedelta(minutes=REFRESH_TOKEN_EXP_MIN)

    # Build claims
    claims = {
        'iss': ISSUER,
        'sub': str(user_id),
        'exp': exp,
        'iat': now,
        'nbf': now,
        'jti': str(uuid4()),
    }

    # Generate token
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

    # Log success
    container['logger'].info(f'Generated refresh token for user_id={user_id}')

    # Return payload
    return {'token': token, 'claims': claims}


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.

    :param token: Encoded JWT string to be decoded and verified.
    
    :returns: Dict with the decoded claims.

    :raises InvalidTokenError: If the token is invalid, expired, missing required claims or any error in decoding.
    """
    try:
        # Decode and validate token
        decoded_token = jwt.decode(token,
                            SECRET_KEY,
                            algorithms=[ALGORITHM],
                            options={'require': ['exp', 'iat', 'jti']},
                            issuer=ISSUER,
                            leeway=5)

    # If token was expired: raise error
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError('Expired token')  # pylint: disable=W0707

    # If token has an invalid signature: raise error
    except jwt.InvalidSignatureError:
        raise InvalidTokenError('Invalid signature')  # pylint: disable=W0707

    # If token has an invalid issuer: raise error
    except jwt.InvalidIssuerError:
        raise InvalidTokenError('Invalid issuer')  # pylint: disable=W0707

    # If token is missing a required claim: raise error
    except jwt.MissingRequiredClaimError as e:
        raise InvalidTokenError(f'Missing required claim: {getattr(e, "claim", "unknown")}')  # pylint: disable=W0707

    # If any other decoding error occurs: raise error
    except Exception as e:
        raise InvalidTokenError(f'Failed to validate token: {e}') from e

    # Get params of token
    jti = decoded_token.get('jti')
    sub = decoded_token.get('sub')

    # If jti or sub not exist: raise error
    if not jti or not sub:
        raise InvalidTokenError('Invalid token')

    # Log success
    container['logger'].info(f'Decoded token jti={decoded_token.get("jti")} for user_id={decoded_token.get("sub")}')

    # Return decoded claims
    return decoded_token
