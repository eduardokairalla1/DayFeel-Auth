"""
Auth endpoints.
"""

# --- IMPORTS ---
from datetime import datetime
from datetime import timezone
from dayfeel_auth.app import container
from dayfeel_auth.db.sqlalchemy.models.auth_sessions import AuthSessions
from dayfeel_auth.utils.auth import decode_token
from dayfeel_auth.utils.auth import generate_access_token
from dayfeel_auth.utils.auth import generate_refresh_token
from dayfeel_auth.utils.security import verify_password
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


# --- TYPES ---
from dayfeel_auth.schemas.endpoints.auth import LoginPayload
from dayfeel_auth.schemas.endpoints.auth import RefreshPayload


# --- GLOBAL ---
# Router instance
router = APIRouter()

# Access token expiration
ACCESS_TOKEN_EXP = container['config'].JWT_ACCESS_TOKEN_EXP_MIN * 60


# --- CODE ---
# Login endpoint
@router.post('/login', response_model = dict)
async def user_login(payload: LoginPayload) -> JSONResponse:
    """
    Login user endpoint.

    :param payload: Validate data input.

    :returns: JSON Response.
    """
    # Log request
    container['logger'].info(f'Login user request "POST /auth/login" received: {payload.email}')

    # Get database repositories
    users_db = container['users_repository']
    auth_db = container['auth_sessions_reposository']

    # Get user from database
    user = users_db.get_by_email(payload.email)

    # If user not found: raise 'HTTP' error
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid credentials!')

    # Get password sent by request
    password = payload.password

    # Get password hash of the found user
    user_hash = user.password_hash

    # Check password
    check = verify_password(password=password, password_hash=user_hash)

    # If check failed: raise 'HTTP' error
    if check is False:
        raise HTTPException(status_code=401, detail='Invalid credentials!')

    # Update last login field of database
    users_db.update_last_login(user_id=user.id)

    # Generate JWT tokens
    access_token = generate_access_token(user_id=user.id, email=user.email, name=user.name, role=user.role.value)
    refresh_token = generate_refresh_token(user_id=user.id)

    # Create a new session
    session = AuthSessions(user_id=user.id,
                           jti=refresh_token['claims']['jti'],
                           expires_at=refresh_token['claims']['exp'])

    # Insert new session to database
    auth_db.insert_session(session)

    # Create endpoint response
    response = {
        'access_token': access_token['token'],
        'refresh_token': refresh_token['token'],
        'token_type': 'Bearer',
        'expires_in': ACCESS_TOKEN_EXP,
        'user': {
            'id': user.id,
            'name': user.name,
            'role': user.role.value
        }
    }

    # Log success
    container['logger'].info('Login user request "POST /auth/login" succeeded with status 200')

    # Return json
    return JSONResponse(content=response, status_code=200)


# Refresh endpoint
@router.post('/refresh', response_model = dict)
async def refresh_tokens(payload: RefreshPayload) -> JSONResponse:
    """
    Refresh JWT tokens endpoint.

    :param payload: Validate data input.

    :returns: JSON Response.
    """
    # Log request
    container['logger'].info('Refresh token request "POST /auth/refresh" received')

    # Decode token
    decoded_token = decode_token(payload.refresh_token)

    # Get database repositories
    user_db = container['users_repository']
    auth_db = container['auth_sessions_reposository']

    # Get jti of JWT token
    jti = decoded_token.get('jti')

    # Get session by jti
    session = auth_db.get_by_jti(jti)

    # If session not found: raise 'HTTP' error
    if not session:
        raise HTTPException(status_code=401, detail='Refresh token not recognized')

    # If token was revoked: raise 'HTTP' error
    if session.revoked:
        raise HTTPException(status_code=401, detail='Refresh token revoked')

    # If token expires: raise 'HTTP' error
    if session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail='Refresh token expired')

    # Revoke the current session
    auth_db.revoke_session(jti)

    # Get user id from token
    user_id = int(decoded_token.get('sub'))

    # Get user by id
    user = user_db.get_by_id(user_id = user_id)

    # If not user: raise 'HTTP' error
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    # Generate new JWT tokens
    access_token = generate_access_token(user_id=user.id, email=user.email, name=user.name, role=user.role.value)
    refresh_token = generate_refresh_token(user_id=user_id)

    # Create new session
    new_session = AuthSessions(user_id=user.id,
                               jti=refresh_token['claims']['jti'],
                               expires_at=refresh_token['claims']['exp'])

    # Insert new session in database
    auth_db.insert_session(new_session)

    # Create endpoint response
    response = {
        'access_token': access_token['token'],
        'refresh_token': refresh_token['token'],
        'token_type': 'Bearer',
        'expires_in': ACCESS_TOKEN_EXP,
        'user': {
            'id': user.id,
            'name': user.name,
            'role': user.role.value
        }
    }

    # Log success
    container['logger'].info('Refresh token request "POST /auth/refresh" succeeded with status 200')

    # Return json
    return JSONResponse(content=response, status_code=200)
