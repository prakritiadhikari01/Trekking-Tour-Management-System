from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'trekking_and_tour_management_system.payments'

    def ready(self):
        from trekking_and_tour_management_system.payments import signals  # noqa: F401
