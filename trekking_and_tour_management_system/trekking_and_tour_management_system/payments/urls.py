from django.urls import path

from trekking_and_tour_management_system.payments.api.views import (
    DownloadInvoiceByPidxView,
    DownloadInvoiceByTokenView,
    InvoiceView,
    KhaltiInitiateView,
    KhaltiVerifyView,
)

urlpatterns = [
    path("initiate/", KhaltiInitiateView.as_view()),
    path("verify/", KhaltiVerifyView.as_view()),
    path("invoice/", InvoiceView.as_view(), name="invoice"),
    path("invoices/<str:token>/download/",DownloadInvoiceByTokenView.as_view(),name="download-invoice",),
    path("download-invoice/<str:pidx>/",DownloadInvoiceByPidxView.as_view(),name="download-invoice-legacy",),
]
  