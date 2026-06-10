from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from trekking_and_tour_management_system.users.permissions import IsAdmin

from trekking_and_tour_management_system.guides.selectors.guide_selectors import (
    get_guide_by_id,
)

from trekking_and_tour_management_system.guides.selectors.guide_statistics_selectors import (
    get_guide_statistics,
)


class GuideStatisticsAPIView(APIView):

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

        return Response(
            get_guide_statistics(
                guide
            )
        )