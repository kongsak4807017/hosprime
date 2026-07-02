import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Core settings
    APP_NAME: str = Field(default="HODT OS")
    DEBUG: bool = Field(default=True)
    # Database URLs
    SQLITE_URL: str = Field(default="sqlite:///./hosprime.db")
    POSTGRES_URL: str = Field(default=os.getenv("POSTGRES_URL", ""))
    # JWT settings
    JWT_SECRET: str = Field(default=os.getenv("JWT_SECRET", "dev-secret-key"))
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRE_MINUTES: int = Field(default=1440)  # 1 day
    # Theme options
    THEME_OPTIONS: list = Field(default=["turquoise", "deepgreen", "bikingred", "burntamber"])
    # Gemini model
    GEMINI_MODEL: str = Field(default="gemini-1.5-pro")
    # Authentication placeholders
    THA_ID_HEADER: str = Field(default="X-THA-ID")
    PROVIDER_ID_HEADER: str = Field(default="X-Provider-ID")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
