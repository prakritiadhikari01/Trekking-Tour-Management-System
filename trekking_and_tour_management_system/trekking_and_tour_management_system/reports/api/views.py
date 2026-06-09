from rest_framework.views import APIView
from rest_framework.response import Response
from reports.services.customer_service import CustomerReportService
from reports.services.package_service import PackageReportService
from reports.services.revenue_service import RevenueReportService
from reports.services.dashboard_service import DashboardService
from reports.selectors.booking_selector import get_total_bookings, get_revenue

class DashboardAPIView(APIView):

    def get(self, request):
        service = DashboardService()
        return Response(service.build())
    
class BookingReportAPIView(APIView):

    def get(self, request):
        return Response({
            "total_bookings": get_total_bookings(),
            "revenue": get_revenue()["total"] or 0,
        })    
class CustomerReportAPIView(APIView):

    def get(self, request):
        service = CustomerReportService()
        return Response(service.build())    
class PackageReportAPIView(APIView):

    def get(self, request):
        return Response(PackageReportService().build())

class RevenueReportAPIView(APIView):

    def get(self, request):
        return Response(RevenueReportService().build())        