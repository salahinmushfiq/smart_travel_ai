# app/tools/booking_tools.py

from app.utils.logger import logger


def create_booking(tour_id: int, user_name: str):
    """
    Placeholder booking tool.
    Later this will call Django booking APIs.
    """

    try:
        logger.info(
            f"[Tool:create_booking] "
            f"user={user_name} | tour_id={tour_id}"
        )

        return {
            "status": "success",
            "message": f"Booking created for {user_name}",
            "booking": {
                "tour_id": tour_id,
                "user_name": user_name
            }
        }

    except Exception as e:
        logger.error(f"[Tool:create_booking Error]: {e}")

        return {
            "status": "error",
            "message": "Booking creation failed."
        }


def cancel_booking(booking_id: int):
    """
    Placeholder booking cancellation.
    """

    try:
        logger.info(
            f"[Tool:cancel_booking] booking_id={booking_id}"
        )

        return {
            "status": "success",
            "message": f"Booking {booking_id} cancelled."
        }

    except Exception as e:
        logger.error(f"[Tool:cancel_booking Error]: {e}")

        return {
            "status": "error",
            "message": "Booking cancellation failed."
        }