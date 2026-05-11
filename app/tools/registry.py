# app/tools/registry.py

from app.tools.tour_tools import (
    list_tours,
    get_tour_details
)

from app.tools.booking_tools import (
    create_booking,
    cancel_booking
)

TOOLS = {

    # =====================================
    # TOUR TOOLS
    # =====================================
    "list_tours": {
        "description": "List available tours",

        "function": list_tours,

        "parameters": {
            "limit": "int"
        },

        "required": []
    },

    "get_tour_details": {
        "description": "Get details about a specific tour",

        "function": get_tour_details,

        "parameters": {
            "tour_name": "str"
        },

        "required": [
            "tour_name"
        ]
    },

    # =====================================
    # BOOKING TOOLS
    # =====================================
    "create_booking": {
        "description": "Create a booking for a tour",

        "function": create_booking,

        "parameters": {
            "tour_id": "int",
            "user_name": "str"
        },

        "required": [
            "tour_id",
            "user_name"
        ]
    },

    "cancel_booking": {
        "description": "Cancel an existing booking",

        "function": cancel_booking,

        "parameters": {
            "booking_id": "int"
        },

        "required": [
            "booking_id"
        ]
    }
}