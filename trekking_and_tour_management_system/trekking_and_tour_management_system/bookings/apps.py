from django.apps import AppConfig


class BookingsConfig(AppConfig):
    name = 'trekking_and_tour_management_system.bookings'

    def ready(self):
        import trekking_and_tour_management_system.bookings.signals