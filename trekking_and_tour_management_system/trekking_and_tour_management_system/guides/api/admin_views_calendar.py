from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from trekking_and_tour_management_system.users.permissions import (
    IsAdmin,
)

from trekking_and_tour_management_system.guides.selectors.guide_selectors import (
    get_guide_by_id,
)

from trekking_and_tour_management_system.guides.selectors.guide_calendar_selectors import (
    get_guide_calendar,
)


class GuideCalendarAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    def get(
        self,
        request,
        guide_id,
    ):

        guide = get_guide_by_id(
            guide_id
        )

        bookings = get_guide_calendar(
            guide
        )

        return Response(
            [
                {
                    "booking_id": booking.id,
                    "package": booking.package.title,
                    "start": booking.trip_start_date,
                    "end": booking.trip_end_date,
                    "status": booking.guide_status,
                }
                for booking in bookings
            ]
        )