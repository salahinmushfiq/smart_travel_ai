# app/tools/booking_tools.py

from app.utils.logger import logger

from app.tools.tool_response import (
    success_response,
    error_response
)


def create_booking(
    tour_id: int,
    user_name: str
):

    try:

        logger.info(
            f"[Tool:create_booking] "
            f"user={user_name} "
            f"| tour_id={tour_id}"
        )

        return success_response(
            tool="create_booking",
            message="Booking created successfully.",
            data={
                "booking": {
                    "tour_id": tour_id,
                    "user_name": user_name
                }
            }
        )

    except Exception as e:

        logger.error(
            f"[Tool:create_booking Error]: {e}"
        )

        return error_response(
            tool="create_booking",
            message="Booking creation failed."
        )


def cancel_booking(
    booking_id: int
):

    try:

        logger.info(
            f"[Tool:cancel_booking] "
            f"booking_id={booking_id}"
        )

        return success_response(
            tool="cancel_booking",
            message=f"Booking {booking_id} cancelled.",
            data={
                "booking_id": booking_id
            }
        )

    except Exception as e:

        logger.error(
            f"[Tool:cancel_booking Error]: {e}"
        )

        return error_response(
            tool="cancel_booking",
            message="Booking cancellation failed."
        )