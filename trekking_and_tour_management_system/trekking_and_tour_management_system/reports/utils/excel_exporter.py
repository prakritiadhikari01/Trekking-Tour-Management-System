
from openpyxl import Workbook
from django.http import HttpResponse


def export_bookings_excel(report_data):

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Bookings Report"

    sheet.append([
        "ID",
        "User",
        "Package",
        "Status",
        "Price",
        "Date"
    ])

    for booking in report_data["data"]:
        sheet.append([
            booking["id"],
            booking["user"],
            booking["package"],
            booking["status"],
            booking["price"],
            str(booking["date"])
        ])

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="bookings_report.xlsx"'
    )

    workbook.save(response)

    return response