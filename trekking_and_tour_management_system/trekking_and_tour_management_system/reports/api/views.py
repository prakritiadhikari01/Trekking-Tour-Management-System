from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from reports.services.customer_service import CustomerReportService
from reports.services.package_service import PackageReportService
from reports.services.revenue_service import RevenueReportService
from reports.services.dashboard_service import DashboardService

from reports.selectors.booking_selector import get_total_bookings, get_revenue
from reports.services.data_builder import get_booking_report_data
from reports.services.report_generator import generate_booking_revenue_pdf
from trekking_and_tour_management_system.reports.services.booking_report_service import generate_booking_report
from trekking_and_tour_management_system.reports.utils.excel_exporter import export_bookings_excel


class DashboardAPIView(APIView):
    def get(self, request):
        return Response(DashboardService().build())


class BookingReportAPIView(APIView):
    def get(self, request):
        return Response({
            "total_bookings": get_total_bookings(),
            "revenue": get_revenue().get("total", 0),
        })


class CustomerReportAPIView(APIView):
    def get(self, request):
        return Response(CustomerReportService().build())


class PackageReportAPIView(APIView):
    def get(self, request):
        return Response(PackageReportService().build())


class RevenueReportAPIView(APIView):
    def get(self, request):
        return Response(RevenueReportService().build())


class RevenueExportPDFView(APIView):
    def get(self, request):
        bookings, revenue = get_booking_report_data()

        pdf_buffer = generate_booking_revenue_pdf(
            bookings,
            revenue
        )

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename="revenue_report.pdf"
        )

class BookingExcelExportView(APIView):

    def get(self, request):

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        status = request.GET.get("status")

        report = generate_booking_report(
            start_date=start_date,
            end_date=end_date,
            status=status,
        )

        return export_bookings_excel(report)
def download_report(request):
    bookings, revenue = get_booking_report_data()

    pdf_buffer = generate_booking_revenue_pdf(bookings, revenue)

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename="booking_report.pdf"
    )