# app/tools/tour_tools.py

import requests
import os
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

DJANGO_API_URL = os.getenv(
    "DJANGO_API_URL",
    "http://localhost:8000/api/tours/public/"
)


def list_tours(limit: int = 5):
    """
    Fetch available tours from Django backend.
    Returns lightweight structured data.
    """

    try:
        response = requests.get(DJANGO_API_URL, timeout=10)

        if response.status_code != 200:
            logger.error(f"[Tool:list_tours] API error: {response.status_code}")

            return {
                "status": "error",
                "message": "Unable to fetch tours."
            }

        tours = response.json()

        formatted = []

        for tour in tours[:limit]:
            formatted.append({
                "id": tour.get("id"),
                "title": tour.get("title"),
                "category": tour.get("category"),
                "price": tour.get("price"),
                "start_location": tour.get("start_location"),
                "end_location": tour.get("end_location"),
                "start_date": tour.get("start_date"),
            })

        return {
            "status": "success",
            "count": len(formatted),
            "data": formatted
        }

    except Exception as e:
        logger.error(f"[Tool:list_tours Error]: {e}")

        return {
            "status": "error",
            "message": "Tour service unavailable."
        }


def get_tour_details(tour_name: str):
    """
    Find a specific tour using title matching.
    """

    try:
        response = requests.get(DJANGO_API_URL, timeout=10)

        if response.status_code != 200:
            return {
                "status": "error",
                "message": "Unable to fetch tour details."
            }

        tours = response.json()

        tour_name = tour_name.lower().strip()

        for tour in tours:
            title = str(tour.get("title", "")).lower()

            if tour_name in title:
                return {
                    "status": "success",
                    "data": {
                        "id": tour.get("id"),
                        "title": tour.get("title"),
                        "description": tour.get("description"),
                        "category": tour.get("category"),
                        "price": tour.get("price"),
                        "start_location": tour.get("start_location"),
                        "end_location": tour.get("end_location"),
                        "start_date": tour.get("start_date"),
                    }
                }

        return {
            "status": "not_found",
            "message": f"No tour found for '{tour_name}'."
        }

    except Exception as e:
        logger.error(f"[Tool:get_tour_details Error]: {e}")

        return {
            "status": "error",
            "message": "Tour detail service unavailable."
        }