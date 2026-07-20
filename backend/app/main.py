import logging
import os

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import api_router
from backend.app.core.config import settings
from backend.app.core.cors import (
    CorsConfigurationError,
    redact_cors_error,
    validate_local_m0_cors_origins,
)
from backend.app.db.models import Base
from backend.app.db.session import engine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def _load_allowed_origins() -> list[str]:
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        '["http://localhost","http://127.0.0.1"]',
    )
    raw_frontend_port = os.getenv("FRONTEND_PORT", "80")
    try:
        frontend_port = int(raw_frontend_port)
        return validate_local_m0_cors_origins(raw_origins, frontend_port)
    except (CorsConfigurationError, TypeError, ValueError) as exc:
        raise RuntimeError(redact_cors_error(exc)) from exc


allowed_origins = _load_allowed_origins()

app = FastAPI(
    title="HosPrime Knowledge Oracle API",
    description="Health Organization Operating System — governed MVP",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def startup_checks() -> None:
    fatal_issues = settings.fatal_configuration_issues()
    if fatal_issues:
        raise RuntimeError(
            "Unsafe runtime configuration: " + "; ".join(fatal_issues)
        )

    security_warnings = settings.security_warnings()
    if security_warnings:
        message = "; ".join(security_warnings)
        if settings.is_production:
            raise RuntimeError(f"Unsafe production configuration: {message}")
        logger.warning("Development security warnings: %s", message)

    capability_warnings = settings.capability_warnings()
    if capability_warnings:
        logger.warning(
            "Optional capabilities unavailable: %s",
            "; ".join(capability_warnings),
        )

    # MVP convenience only. Production must use Alembic migrations and a
    # controlled deployment job rather than create_all at application startup.
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema is available on dialect: %s", engine.dialect.name)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database_dialect": engine.dialect.name,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health/live")
def health_live():
    return {"status": "live"}


@app.get("/health/ready")
def health_ready():
    fatal_issues = settings.fatal_configuration_issues()
    security_warnings = settings.security_warnings()
    if fatal_issues or (settings.is_production and security_warnings):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "configuration_issues": security_warnings,
            },
        )
    return {
        "status": "ready" if not security_warnings else "degraded",
        "configuration_warnings": security_warnings,
        "capability_warnings": settings.capability_warnings(),
        "database_dialect": engine.dialect.name,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=not settings.is_production,
    )
