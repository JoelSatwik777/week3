from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from backend.config.settings import get_settings
from backend.routers.health import router as health_router
from backend.routers.prediction import router as prediction_router
from backend.utils.errors import ServiceError
from backend.utils.logging import configure_logging, get_logger


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url='/docs',
        redoc_url='/redoc',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(health_router)
    app.include_router(prediction_router)
    app.include_router(health_router, prefix='/api/v1')
    app.include_router(prediction_router, prefix='/api/v1')

    logger = get_logger(__name__)

    @app.exception_handler(ServiceError)
    async def service_error_handler(_, exc: ServiceError):
        logger.error('Service error: %s', exc.message)
        return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(_, exc: ValidationError):
        logger.warning('Validation error: %s', exc)
        return JSONResponse(status_code=422, content={'detail': exc.errors()})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_, exc: Exception):
        logger.exception('Unhandled server error: %s', exc)
        return JSONResponse(status_code=500, content={'detail': 'Internal server error.'})

    return app


app = create_app()
