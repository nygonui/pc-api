from collections.abc import Awaitable, Callable

import secure
from fastapi import Request, Response

secure_headers = secure.Secure.from_preset(secure.Preset.BASIC)


async def secure_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    FastAPI middleware to apply security headers to responses.

    This middleware intercepts incoming requests, processes them via the next
    middleware or route handler, and then applies a set of predefined
    security headers to the response before it's sent back to the client.

    Args:
        request: The incoming FastAPI Request object.
        call_next: A callable that represents the next middleware or route
                   handler in the chain. It takes a Request and returns
                   an Awaitable that resolves to a Response.

    Returns:
        The Response object with security headers applied.
    """
    response = await call_next(request)
    secure_headers.set_headers(response)  # pyright: ignore[reportArgumentType]
    return response
