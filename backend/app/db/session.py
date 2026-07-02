import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ค้นหาว่าควรใช้ฐานข้อมูลใด (PostgreSQL / SQLite)
db_url = settings.DATABASE_URL
if settings.POSTGRES_URL:
    db_url = settings.POSTGRES_URL

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    logger.info(f"Initializing database engine on: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    engine = create_engine(db_url, connect_args=connect_args)
    # ทดสอบการเชื่อมต่อ
    with engine.connect() as conn:
        pass
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.error(f"Failed to connect to primary DB: {e}. Falling back to SQLite.")
    # Fallback to default SQLite
    db_url = "sqlite:///./hosprime.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
