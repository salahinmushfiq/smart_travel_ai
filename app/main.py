# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
import os
import uvicorn
from app.services.data_ingestion import ingest_tours
from app.utils.logger import logger

app = FastAPI(title="Smart Travel AI Assistant")

# Allow your frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for live deployment
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, GET, etc.
    allow_headers=["*"],  # Allow all headers
)

# Include chat routes
app.include_router(chat.router)


@app.get("/")
def root():
    return {"message": "Hello! Smart Travel AI Assistant backend is running."}


@app.get("/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}! Welcome to your AI assistant."}


@app.on_event("startup")
def startup_event():
    logger.info("Starting app...")

    try:
        ingest_tours()
    except Exception as e:
        logger.error(f"[Startup Ingestion Failed]: {e}")
