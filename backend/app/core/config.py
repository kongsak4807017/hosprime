import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Runtime environment
    ENVIRONMENT: str = "development"
    APP_NAME: str = "HosPrime"
    APP_VERSION: str = "1.1.0"

    # AI providers: credentials must be supplied through environment variables.
    GEMINI_API_KEY: str = ""
    GEMINI_GENERATION_MODEL: str = "gemini-2.5-flash"
    GEMINI_PRO_MODEL: str = "gemini-2.5-pro"
    GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-001"

    # Unsafe demo fallbacks are disabled by default. When enabled, generated
    # content must never be treated as organizational evidence.
    ALLOW_DEMO_FALLBACKS: bool = False
    ALLOW_PSEUDO_EMBEDDINGS: bool = False

    # Data stores
    DATABASE_URL: str = "sqlite:///./hosprime.db"
    POSTGRES_URL: str = ""
    REDIS_URL: str = ""
    NEO4J_URI: str = ""
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    # Authentication and security
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Storage and upload controls
    STORAGE_DIR: str = "../storage"
    DOCUMENT_DIR: str = "../storage/documents"
    INDEX_DIR: str = "../storage/indexes"
    MAX_UPLOAD_BYTES: int = 25 * 1024 * 1024

    # Network
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() in {"production", "prod"}

    def security_warnings(self) -> list[str]:
        warnings: list[str] = []
        if not self.JWT_SECRET:
            warnings.append("JWT_SECRET is not configured")
        if not self.GEMINI_API_KEY:
            warnings.append("GEMINI_API_KEY is not configured")
        if self.ALLOW_DEMO_FALLBACKS:
            warnings.append("ALLOW_DEMO_FALLBACKS is enabled")
        if self.ALLOW_PSEUDO_EMBEDDINGS:
            warnings.append("ALLOW_PSEUDO_EMBEDDINGS is enabled")
        return warnings


settings = Settings()

# Create only local directories. Production deployments should mount managed
# object storage or persistent volumes at these paths.
for directory in (settings.STORAGE_DIR, settings.DOCUMENT_DIR, settings.INDEX_DIR):
    Path(directory).mkdir(parents=True, exist_ok=True)
