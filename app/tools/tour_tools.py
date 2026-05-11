# app/tools/tour_tools.py

import requests
import os

from dotenv import load_dotenv

from app.utils.logger import logger

from app.tools.tool_response import (
    success_response,
    error_response
)

load_dotenv()

DJANGO_API_URL = os.getenv(
    "DJANGO_API_URL",
    "http://localhost:8000/api/tours/public/"
)


def list_tours(limit: int = 5):

    try:

        response = requests.get(
            DJANGO_API_URL,
            timeout=10
        )

        if response.status_code != 200:

            logger.error(
                f"[Tool:list_tours] "
                f"API error: {response.status_code}"
            )

            return error_response(
                tool="list_tours",
                message="Unable to fetch tours."
            )

        tours = response.json()

        formatted = []

        for tour in tours[:limit]:

            formatted.append({
                "id": tour.get("id"),
                "title": tour.get("title"),
                "category": tour.get("category"),
                "cost_per_person": tour.get("cost_per_person"),
                "start_location": tour.get("start_location"),
                "end_location": tour.get("end_location"),
                "start_date": tour.get("start_date"),
            })

        return success_response(
            tool="list_tours",
            message="Tours fetched successfully.",
            data={
                "count": len(formatted),
                "tours": formatted
            }
        )

    except Exception as e:

        logger.error(
            f"[Tool:list_tours Error]: {e}"
        )

        return error_response(
            tool="list_tours",
            message="Tour service unavailable."
        )


def get_tour_details(tour_name: str):

    try:

        response = requests.get(
            DJANGO_API_URL,
            timeout=10
        )

        if response.status_code != 200:

            return error_response(
                tool="get_tour_details",
                message="Unable to fetch tour details."
            )

        tours = response.json()

        cleaned_name = tour_name.lower().strip()

        for tour in tours:

            title = str(
                tour.get("title", "")
            ).lower()

            if cleaned_name in title:

                return success_response(
                    tool="get_tour_details",
                    message="Tour found.",
                    data={
                        "tour": {
                            "id": tour.get("id"),
                            "title": tour.get("title"),
                            "description": tour.get("description"),
                            "category": tour.get("category"),
                            "cost_per_person": tour.get("cost_per_person"),
                            "start_location": tour.get("start_location"),
                            "end_location": tour.get("end_location"),
                            "start_date": tour.get("start_date"),
                        }
                    }
                )

        return error_response(
            tool="get_tour_details",
            message=f"No tour found for '{tour_name}'."
        )

    except Exception as e:

        logger.error(
            f"[Tool:get_tour_details Error]: {e}"
        )

        return error_response(
            tool="get_tour_details",
            message="Tour detail service unavailable."
        )