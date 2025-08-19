from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.exc import APIError, api_error_handler
from app.api.routes import router
from app.api.secure import secure_middleware
from app.settings import LOCAL, SERVER_HOST, SERVER_PORT, WORKERS

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for FastAPI"""
#     database.warm()
#     app.state._state = {}
#     yield
#     del app.state._state


def get_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.

    This function sets up the basic metadata for the API
    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Pioneiros da Colina",
        description="Pioneiros da Colina API for pathfinders management",
        version="0.1.0",
        contact={
            "name": "Pioneiros da colina",
            "email": "dev@rezendevitor.gmail.com",
            "url": "https://clubes.adventistas.org/br/aps/14062/pioneiros-da-colina/",
        },
        openapi_url="/openapi.json" if LOCAL else None,
        docs_url="/docs" if LOCAL else None,
        redoc_url=None,
        default_response_class=ORJSONResponse,
        # lifespan=lifespan,
    )
    app.add_exception_handler(APIError, api_error_handler)  # pyright: ignore[reportArgumentType]]
    app.add_middleware(BaseHTTPMiddleware, dispatch=secure_middleware)
    app.include_router(router=router)
    return app


app = get_app()

if __name__ == "__main__":
    from granian.constants import Interfaces
    from granian.log import LogLevels
    from granian.server import Server

    Server(
        "app.main:app",
        address=SERVER_HOST,
        port=SERVER_PORT,
        reload=False,
        interface=Interfaces.ASGI,
        log_access=True,
        log_level=LogLevels.info,
        workers=WORKERS,
    ).serve()
