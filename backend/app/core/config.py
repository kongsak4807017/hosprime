import os
from pathlib import Path
from urllib.parse import urlparse

from pydantic_settings import BaseSettings, SettingsConfigDict


_PLACEHOLDER_MARKERS = (
    "change_me",
    "changeme",
    "replace_me",
    "replace-with",
    "example",
)
_KNOWN_UNSAFE_SECRETS = {
    "secret",
    "password",
    "postgrespassword",
    "neo4jpassword",
    "hosprime-super-secret-key-enterprise",
    "admin1234",
    "user1234",
}


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
    SEED_DEMO_DATA: bool = False

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
    BOOTSTRAP_ADMIN_USERNAME: str = "admin"
    BOOTSTRAP_ADMIN_PASSWORD: str = ""

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

    @property
    def effective_database_url(self) -> str:
        """Return the database URL used by the SQLAlchemy session layer."""
        return self.POSTGRES_URL or self.DATABASE_URL

    @staticmethod
    def _is_placeholder(value: str) -> bool:
        normalized = value.strip().lower()
        return any(marker in normalized for marker in _PLACEHOLDER_MARKERS)

    @staticmethod
    def _is_known_unsafe_secret(value: str) -> bool:
        return value.strip().lower() in _KNOWN_UNSAFE_SECRETS

    @staticmethod
    def _url_contains_unsafe_password(value: str) -> bool:
        try:
            password = urlparse(value).password or ""
        except ValueError:
            return True
        return bool(password) and (
            Settings._is_placeholder(password)
            or Settings._is_known_unsafe_secret(password)
        )

    def fatal_configuration_issues(self) -> list[str]:
        """Return configuration defects that must stop every runtime."""
        issues: list[str] = []
        secret_values = {
            "JWT_SECRET": self.JWT_SECRET,
            "GEMINI_API_KEY": self.GEMINI_API_KEY,
            "NEO4J_PASSWORD": self.NEO4J_PASSWORD,
            "BOOTSTRAP_ADMIN_PASSWORD": self.BOOTSTRAP_ADMIN_PASSWORD,
        }
        for name, value in secret_values.items():
            if value and (
                self._is_placeholder(value) or self._is_known_unsafe_secret(value)
            ):
                issues.append(f"{name} contains an insecure placeholder or known default")

        if self.JWT_SECRET and len(self.JWT_SECRET) < 32:
            issues.append("JWT_SECRET must contain at least 32 characters")
        if not self.BOOTSTRAP_ADMIN_PASSWORD:
            issues.append("BOOTSTRAP_ADMIN_PASSWORD is not configured")
        elif len(self.BOOTSTRAP_ADMIN_PASSWORD) < 12:
            issues.append("BOOTSTRAP_ADMIN_PASSWORD must contain at least 12 characters")
        if not self.BOOTSTRAP_ADMIN_USERNAME.strip():
            issues.append("BOOTSTRAP_ADMIN_USERNAME is not configured")

        for name, value in {
            "DATABASE_URL": self.DATABASE_URL,
            "POSTGRES_URL": self.POSTGRES_URL,
        }.items():
            if value and self._url_contains_unsafe_password(value):
                issues.append(f"{name} contains an insecure database password")
        return issues

    def security_warnings(self) -> list[str]:
        """Return security defects that make production unsafe or local readiness degraded."""
        warnings = self.fatal_configuration_issues()
        if not self.JWT_SECRET:
            warnings.append("JWT_SECRET is not configured")
        if not self.NEO4J_PASSWORD:
            warnings.append("NEO4J_PASSWORD is not configured")
        if self.ALLOW_DEMO_FALLBACKS:
            warnings.append("ALLOW_DEMO_FALLBACKS is enabled")
        if self.ALLOW_PSEUDO_EMBEDDINGS:
            warnings.append("ALLOW_PSEUDO_EMBEDDINGS is enabled")
        if self.SEED_DEMO_DATA:
            warnings.append("SEED_DEMO_DATA is enabled")
        if self.is_production and self.effective_database_url.startswith("sqlite:"):
            warnings.append("SQLite is not permitted in production")
        return list(dict.fromkeys(warnings))

    def capability_warnings(self) -> list[str]:
        """Return unavailable optional capabilities without degrading core readiness."""
        warnings: list[str] = []
        if not self.GEMINI_API_KEY:
            warnings.append("External AI provider is not configured")
        return warnings


settings = Settings()

# Create only local directories. Production deployments should mount managed
# object storage or persistent volumes at these paths.
for directory in (settings.STORAGE_DIR, settings.DOCUMENT_DIR, settings.INDEX_DIR):
    Path(directory).mkdir(parents=True, exist_ok=True)
