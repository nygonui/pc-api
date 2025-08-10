from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.exc import APIError, api_error_handler
from app.api.routes import router
from app.api.secure import secure_middleware
from app.settings import LOCAL, LOG_LEVEL, SERVER_HOST, SERVER_PORT

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Lifespan event handler for FastAPI"""
#     database.warm()
#     app.state._state = {}
#     yield
#     del app.state._state


def get_app() -> FastAPI:
    app = FastAPI(
        title="Pioneiros da Colina",
        description="Pioneiros da Colina API for pathfinders management",
        version="0.1.0",
        contact={
            "name": "Riza",
            "email": "infra@rizaasset.com",
            "url": "https://rizaasset.com",
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
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=LOCAL,
        log_level=LOG_LEVEL,
    )
