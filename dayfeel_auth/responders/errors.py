"""
Responder's error handlers.
"""

# --- IMPORTS ---
from dayfeel_auth.app import app
from dayfeel_auth.app import container
from dayfeel_auth.err.already_exists_error import AlreadyExistsError
from dayfeel_auth.err.database_unavailable_error import DatabaseUnavailableError
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# --- CODE ---
@app.exception_handler(AlreadyExistsError)
async def already_exists_error_handler(
    request: Request,  # pylint: disable=W0613
    error: AlreadyExistsError
) -> JSONResponse:
    """
    Handle AlreadyExistsError exceptions.

    :param request: http request.
    :param error: AlreadyExistsError instance.

    :returns: JSONResponse with 'error' field describing the exception.
    """
    # get error parameters
    entity = error.args[1].get('entity')
    local = error.args[1].get('local')
    detail = error.args[1].get('detail')

    # log error
    container['logger'].error(f'The {entity} already exists in {local}: {detail}')

    # fail request
    return JSONResponse(
        {'error': error.message},
        status_code = 409,
    )


@app.exception_handler(DatabaseUnavailableError)
async def database_unavailable_error_handler(
    request: Request,  # pylint: disable=W0613
    error: DatabaseUnavailableError
) -> JSONResponse:
    """
    Handle DatabaseUnavailableError exceptions.

    :param request: http request.
    :param error: DatabaseUnavailableError instance.

    :returns: JSONResponse with 'error' field describing the exception.
    """
    # get error parameters
    detail = error.args[1]

    # log errors
    container['logger'].error(f'Database failed: {detail}')

    # fail request
    return JSONResponse(
        {'error': error.message},
        status_code = 503,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    error: HTTPException
) -> JSONResponse:
    """
    Handle HTTPException exceptions.

    :param request: http request.
    :param error: HTTPException instance.

    :returns: JSONResponse with 'error' field describing the exception.
    """
    # get error parameters
    method = request.scope['method']
    path = request.scope['path']
    status = error.status_code
    detail = error.detail.get('error')

    # log errors
    container['logger'].error(f'Request "{method} {path}" failed with {status}: {detail}')

    # fail request
    return JSONResponse(
        {'error': error.detail.get('error')},
        status_code = error.status_code,
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request,
    error: RequestValidationError
) -> JSONResponse:
    """
    Handle RequestValidationError exceptions.

    :param request: http request.
    :param error: exception instance.

    :returns: properly formatted JSONResponse
    """

    # Initialize list with all errors.
    errors = []

    # Get request body validation errors.
    for err in error.errors():

        # Get full error path.
        path = ' -> '.join(map(str, err['loc'][1:]))

        # Add error to errors list.
        errors.append(f'{path}: {err["msg"]}')

    # get error parameters
    method = request.scope['method']
    path = request.scope['path']
    status = 422
    detail = '\n'.join(errors)

    # log errors
    container['logger'].error(f'Validation request "{method} {path}" failed with status {status}: {detail}')

    # Return proper error message.
    return JSONResponse({'error': '\n'.join(errors)}, status_code = 422)
