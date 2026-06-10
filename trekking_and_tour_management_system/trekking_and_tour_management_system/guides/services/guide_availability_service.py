#app/guides/services/guide_availability_service.py
from trekking_and_tour_management_system.guides.selectors.guide_assignment_selectors import (
    get_booking_for_assignment,
)

from trekking_and_tour_management_system.guides.selectors.guide_availability_selectors import (
    get_available_guides_for_booking,
)


class GuideAvailabilityService:

    @staticmethod
    def get_available_guides(
        booking_id,
    ):
        booking = get_booking_for_assignment(
            booking_id
        )

        return get_available_guides_for_booking(
            booking
        )