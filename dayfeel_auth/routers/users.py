"""
Users endpoints.
"""

# --- IMPORTS ---
from dayfeel_auth.app import container
from dayfeel_auth.db.sqlalchemy.models.users import Users
from dayfeel_auth.utils.security import hash_password
from fastapi import APIRouter
from fastapi.responses import JSONResponse


# --- TYPES ---
from dayfeel_auth.schemas.endpoints.users import RegisterPayload


# --- GLOBAL ---
# Router instance
router = APIRouter()


# --- CODE ---
# Register user endpoint
@router.post('/register', response_model = dict)
async def register_user(payload: RegisterPayload) -> JSONResponse:
    """
    Register user endpoint.

    :param payload: Validate data input.

    :returns: JSON Response.
    """

    container['logger'].info('Register user request "POST /auth/register" received')

    # Get users database repository
    db = container['users_repository']

    # Generate a password hash
    password_hash = hash_password(password=payload.password)

    # Create user model instance
    new_user = Users(email=payload.email, password_hash=password_hash, name=payload.name)

    # Add user to database
    user = db.insert_user(user=new_user)

    # Create endpoint response
    response = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role.value
    }

    container['logger'].info('Register user request "POST /auth/register" succeeded with status 201')

    # Return json
    return JSONResponse(content=response, status_code=201)
