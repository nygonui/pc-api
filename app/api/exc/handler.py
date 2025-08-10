from fastapi import Request, Response
from fastapi.responses import ORJSONResponse

from .exceptions import APIError


async def api_error_handler(_: Request, exc: APIError) -> Response:
    """
    Handles APIError exceptions and returns an ORJSONResponse.

    This function acts as an exception handler for `APIError` instances.
    It converts the error details into a JSON response, sets the appropriate
    HTTP status code, and includes an 'X-Error' header with the error message.

    :param _: The incoming request object (unused).
    :param exc: The APIError exception instance to be handled.
    :return: An ORJSONResponse containing the error details from `exc.to_dict()`,
             with the status code from `exc.status_code`, and an 'X-Error' header.
    """
    return ORJSONResponse(
        exc.to_dict(), status_code=exc.status_code, headers={"X-Error": exc.message}
    )
