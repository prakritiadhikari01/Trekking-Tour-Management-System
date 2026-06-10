from django.db.models import Count

from trekking_and_tour_management_system.guides.models import Guide


def get_guide_workloads():

    return Guide.objects.annotate(
        active_assignments=Count(
            "assigned_bookings"
        )
    )