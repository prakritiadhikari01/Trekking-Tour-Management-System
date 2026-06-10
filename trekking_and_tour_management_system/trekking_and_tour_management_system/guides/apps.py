from django.apps import AppConfig


class GuidesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trekking_and_tour_management_system.guides'
    def ready(self):
        import trekking_and_tour_management_system.guides.signals