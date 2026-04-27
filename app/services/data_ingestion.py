# app/services/data_ingestion.py
import requests
import os
from app.utils.vector_db import add_documents_to_db, delete_by_source
from app.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()
DJANGO_API_URL_PREFIX = os.getenv("DJANGO_API_URL")
DJANGO_API_URL = DJANGO_API_URL_PREFIX+"/api/tours/public/"


def fetch_tours():
    try:
        response = requests.get(DJANGO_API_URL, timeout=10)

        if response.status_code != 200:
            logger.error(f"[Ingestion] Django error: {response.status_code}")
            return []

        return response.json()

    except Exception as e:
        logger.error(f"[Ingestion Fetch Error]: {e}")
        return []


def transform_tours_to_docs(tours):
    docs = []

    for tour in tours:
        content = f"""
Tour: {tour.get('title', '')}
Category: {tour.get('category', '')}
Route: {tour.get('start_location', '')} → {tour.get('end_location', '')}
Price: {tour.get('price', 0)} BDT
Date: {tour.get('start_date', '')}

Description:
{tour.get('description', '')}
""".strip()

        docs.append({
            "id": f"tour_{tour.get('id')}",
            "content": content,
            "metadata": {
                "source": "django",
                "category": tour.get("category", ""),
                "location": tour.get("start_location", "")
            }
        })

    return docs


def ingest_tours():
    logger.info("[Ingestion] Syncing Django tours...")

    tours = fetch_tours()

    if not tours:
        logger.warning("[Ingestion] No tours found.")
        return

    delete_by_source("django")

    docs = transform_tours_to_docs(tours)
    add_documents_to_db(docs)

    logger.info(f"[Ingestion] Synced {len(docs)} tours")