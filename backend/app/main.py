import json
import logging
import os

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import api_router
from backend.app.core.config import settings
from backend.app.db.models import Base
from backend.app.db.session import engine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="HosPrime Knowledge Oracle API",
    description="Health Organization Operating System — governed MVP",
    version=settings.APP_VERSION,
)

cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    try:
        allowed_origins = json.loads(cors_origins_env)
    except Exception:
        allowed_origins = [
            origin.strip()
            for origin in cors_origins_env.split(",")
            if origin.strip()
        ]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

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
    warnings = settings.security_warnings()
    if warnings:
        message = "; ".join(warnings)
        if settings.is_production:
            raise RuntimeError(f"Unsafe production configuration: {message}")
        logger.warning("Development configuration warnings: %s", message)

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
    warnings = settings.security_warnings()
    if settings.is_production and warnings:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "configuration_issues": warnings},
        )
    return {
        "status": "ready" if not warnings else "degraded",
        "configuration_warnings": warnings,
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
