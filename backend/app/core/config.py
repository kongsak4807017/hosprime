import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = "AIzaSyDGql9VM_5aWG-i57xLchiueyM2GkuN9nc"
    DATABASE_URL: str = "sqlite:///./hosprime.db"
    POSTGRES_URL: str = ""
    REDIS_URL: str = ""
    NEO4J_URI: str = ""
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""
    JWT_SECRET: str = "dev-secret-key"
    JWT_ALGORITHM: str = "HS256"
    STORAGE_DIR: str = "../storage"
    DOCUMENT_DIR: str = "../storage/documents"
    INDEX_DIR: str = "../storage/indexes"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# ตรวจสอบและสร้าง Directory ที่จำเป็นสำหรับเก็บไฟล์และ Vector Index
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(settings.DOCUMENT_DIR, exist_ok=True)
os.makedirs(settings.INDEX_DIR, exist_ok=True)
