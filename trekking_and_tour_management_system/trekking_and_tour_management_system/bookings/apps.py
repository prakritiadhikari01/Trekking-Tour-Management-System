from django.apps import AppConfig


class BookingsConfig(AppConfig):
    name = 'trekking_and_tour_management_system.bookings'

    def ready(self):
        from trekking_and_tour_management_system.bookings import signals  # noqa: F401
