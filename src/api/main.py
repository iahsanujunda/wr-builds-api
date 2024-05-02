import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.utils.logging import configure_logging
from src.config.app_config import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    # initialize app
    app = FastAPI(title="WR Builds API",
                  version='0.0.1')

    # setup logging
    configure_logging()

    # configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["*"],
    )

    @app.exception_handler(RequestValidationError)
    def req_validation_error_handling(request, exc: RequestValidationError):
        logger.info(str(exc.errors()))
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    # add root route
    @app.get("/")
    def root_route_handler():
        return {"message": "server is up"}

    return app
