# app/tools/tool_router.py

import re


def detect_tool(question: str):
    """
    Lightweight deterministic tool router.

    Returns:
    {
        "mode": "tool" | "rag",
        "tool": tool_name or None,
        "params": {}
    }
    """

    q = question.lower().strip()

    # =====================================
    # LIST TOURS
    # =====================================
    list_patterns = [
        "list tours",
        "show tours",
        "available tours",
        "show me tours",
        "what tours are available",
        "travel packages",
    ]

    if any(p in q for p in list_patterns):
        return {
            "mode": "tool",
            "tool": "list_tours",
            "params": {
                "limit": 5
            }
        }

    # =====================================
    # TOUR DETAILS
    # =====================================
    detail_patterns = [
        "tell me about",
        "details about",
        "tour details",
        "information about",
    ]

    if any(p in q for p in detail_patterns):

        cleaned = q

        for p in detail_patterns:
            cleaned = cleaned.replace(p, "")

        cleaned = cleaned.strip()

        if cleaned:
            return {
                "mode": "tool",
                "tool": "get_tour_details",
                "params": {
                    "tour_name": cleaned
                }
            }

    # =====================================
    # CREATE BOOKING
    # =====================================
    booking_patterns = [
        "book",
        "reserve",
        "create booking",
    ]

    if any(p in q for p in booking_patterns):

        tour_id_match = re.search(r"\d+", q)

        return {
            "mode": "tool",
            "tool": "create_booking",
            "params": {
                "tour_id": int(tour_id_match.group()) if tour_id_match else 1,
                "user_name": "demo_user"
            }
        }

    # =====================================
    # CANCEL BOOKING
    # =====================================
    cancel_patterns = [
        "cancel booking",
        "cancel reservation",
    ]

    if any(p in q for p in cancel_patterns):

        booking_id_match = re.search(r"\d+", q)

        return {
            "mode": "tool",
            "tool": "cancel_booking",
            "params": {
                "booking_id": int(booking_id_match.group()) if booking_id_match else 1
            }
        }

    # =====================================
    # DEFAULT → RAG
    # =====================================
    return {
        "mode": "rag",
        "tool": None,
        "params": {}
    }