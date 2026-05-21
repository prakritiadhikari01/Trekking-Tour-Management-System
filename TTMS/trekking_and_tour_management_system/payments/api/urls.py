from django.urls import path

from .views import KhaltiInitiateView, KhaltiVerifyView, payment_success

urlpatterns = [
    path("initiate/", KhaltiInitiateView.as_view()),
    path("verify/", KhaltiVerifyView.as_view()),
    path("payment/success/", payment_success, name="payment-success"),

]