from django.apps import AppConfig


class GuideApplicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trekking_and_tour_management_system.guide_applications"

    def ready(self):
        import trekking_and_tour_management_system.guide_applications.services.signals