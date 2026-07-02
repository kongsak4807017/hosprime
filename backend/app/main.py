import os
import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.db.session import engine
from backend.app.db.models import Base
from backend.app.api.router import api_router

# ตั้งค่า Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# สร้างตารางในฐานข้อมูล SQLite (หากไม่มีอยู่)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize database tables: {e}")

app = FastAPI(
    title="HosPrime Knowledge Oracle API",
    description="Health Organization Operating System (Milestone 1: Knowledge Oracle MVP) Backend Engine",
    version="1.0.0"
)

# ตั้งค่า CORS (Cross-Origin Resource Sharing)
cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    try:
        allowed_origins = json.loads(cors_origins_env)
    except Exception:
        allowed_origins = [origin.strip() for origin in cors_origins_env.split(",")]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# เชื่อมโยง API Routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app_name": "HosPrime Knowledge Oracle MVP Backend",
        "version": "1.0.0",
        "database": "SQLite Connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
