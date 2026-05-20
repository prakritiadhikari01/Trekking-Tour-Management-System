from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("khalti/<int:booking_id>/", views.khalti_payment, name="khalti_payment"),
    path("success/", views.payment_success, name="payment_success"),
    path("failed/", views.payment_failed, name="payment_failed"),
]