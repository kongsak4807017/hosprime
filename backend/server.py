from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import logging
import os

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.database import client
from core.seed import seed_all
from routes.appointments import router as appointments_router
from routes.auth import router as auth_router
from routes.billing import router as billing_router
from routes.dashboard import router as dashboard_router
from routes.lab import router as lab_router
from routes.patients import router as patients_router
from routes.pharmacy import router as pharmacy_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="HosPRIME API", version="1.0.0")

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "HosPRIME API", "version": "1.0.0", "status": "operational"}


api_router.include_router(auth_router)
api_router.include_router(patients_router)
api_router.include_router(appointments_router)
api_router.include_router(dashboard_router)
api_router.include_router(pharmacy_router)
api_router.include_router(lab_router)
api_router.include_router(billing_router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await seed_all()
    logger.info("HosPRIME backend started")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
