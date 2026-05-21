from django.urls import path

from .views import KhaltiInitiateView, KhaltiVerifyView

urlpatterns = [
    path("initiate/", KhaltiInitiateView.as_view()),
    path("verify/", KhaltiVerifyView.as_view()),
    
]