# guides/selectors/guide_selectors.py
from trekking_and_tour_management_system.guides.models import Guide


def get_guide_by_id(
    guide_id,
):
    return Guide.objects.select_related(
        "user"
    ).get(
        id=guide_id
    )