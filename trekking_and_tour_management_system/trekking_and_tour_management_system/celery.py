import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "trekking_and_tour_management_system.settings"
)

app = Celery("trekking_and_tour_management_system")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()