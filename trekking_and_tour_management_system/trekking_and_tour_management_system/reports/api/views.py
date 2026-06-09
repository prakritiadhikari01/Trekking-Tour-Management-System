from rest_framework.views import APIView
from rest_framework.response import Response

from reports.services.booking_report_service import (
    generate_booking_report,
    generate_revenue_report
)
from trekking_and_tour_management_system.guide_applications.permissions import IsAdminUser
from trekking_and_tour_management_system.reports.services.dashboard_service import get_dashboard_data

from reports.services.customer_report_services import generate_customer_report
from trekking_and_tour_management_system.reports.services.package_report_service import generate_package_report

class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(
            get_dashboard_data()
        )
    
class BookingReportView(APIView):

    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        status = request.GET.get("status")

        data = generate_booking_report(start_date, end_date, status)

        return Response({
            "success": True,
            "data": data
        })


class RevenueReportView(APIView):

    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        data = generate_revenue_report(start_date, end_date)

        return Response({
            "success": True,
            "data": data
        })
    
class CustomerReportAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = generate_customer_report()

        return Response({
            "success": True,
            "data": data
        })
    
class PackageReportAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = generate_package_report()

        return Response({
            "success": True,
            "data": data
        })    