from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat
from app.services.data_ingestion import ingest_tours
from app.utils.logger import logger
import os


# =========================
# STARTUP LIFECYCLE
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        logger.info("Starting ingestion...")

        ingest_tours()

        logger.info("Ingestion completed.")

    except Exception as e:
        logger.error(f"Startup ingestion failed: {e}")

    yield

    logger.info("Shutting down...")


# =========================
# APP
# =========================
app = FastAPI(
    title="Smart Travel AI Assistant",
    lifespan=lifespan
)

ALLOW_ORIGIN = os.getenv(
    "ALLOW_ORIGIN",
    "http://localhost:5173"
).split(",")


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================
app.include_router(chat.router)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "Smart Travel AI Assistant is running 🚀"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# OPTIONAL MANUAL INGEST
# =========================
@app.get("/ingest")
def trigger_ingestion():

    try:
        ingest_tours()

        return {"status": "ingested successfully"}

    except Exception as e:

        logger.error(f"Ingestion failed: {e}")

        return {
            "status": "failed",
            "error": str(e)
        }