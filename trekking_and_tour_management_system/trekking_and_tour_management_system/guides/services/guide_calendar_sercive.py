
class GuideCalendarService:
    @staticmethod
    def get_guide_calendar(guide):
        from trekking_and_tour_management_system.guides.selectors.guide_calendar_selectors import (
            get_guide_calendar,
        )

        return get_guide_calendar(guide)