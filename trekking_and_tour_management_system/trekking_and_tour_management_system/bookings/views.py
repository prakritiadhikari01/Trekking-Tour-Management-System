from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from trekking_and_tour_management_system.packages.models import TrekPackage

from .forms import BookingForm
from .models import Booking

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from bookings.models import Booking
from payments.models import Payment
from bookings.api.serializers import BookingHistorySerializer

def booking_home(request):
    packages = TrekPackage.objects.all()
    return render(request, "bookings/home.html", {
        "packages": packages
    })
@login_required
def create_booking(request, slug):

    package = get_object_or_404(
        TrekPackage,
        slug=slug
    )

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.user = request.user
            booking.package = package

            booking.total_price = (
                package.price *
                booking.number_of_people
            )

            booking.save()

            return redirect(
                "bookings:booking_success"
            )

    else:
        form = BookingForm()

    context = {
        "form": form,
        "package": package,
    }

    return render(
        request,
        "bookings/booking_form.html",
        context
    )


@login_required
def booking_success(request):

    return render(
        request,
        "bookings/booking_success.html"
    )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    )

    context = {
        "bookings": bookings
    }

    return render(
        request,
        "bookings/my_bookings.html",
        context
    )
