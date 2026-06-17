from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def build_booking_revenue_pdf(title, bookings_data, total_revenue, start_date=None, end_date=None):
    """
    Clean production-ready PDF generator (NO ORM logic inside)
    """

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # ================= HEADER =================
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, title)

    p.setFont("Helvetica", 10)
    p.drawString(50, height - 75, f"Generated At: {start_date} to {end_date}" if start_date and end_date else "Generated Report")

    # ================= SUMMARY =================
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 110, f"Total Revenue: NPR {total_revenue}")

    # ================= TABLE HEADER =================
    y = height - 150
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Booking ID")
    p.drawString(150, y, "User")
    p.drawString(350, y, "Price")

    y -= 20
    p.setFont("Helvetica", 10)

    # ================= TABLE ROWS =================
    for row in bookings_data:
        # row = {id, user, price}
        p.drawString(50, y, str(row["id"]))
        p.drawString(150, y, str(row["user"]))
        p.drawString(350, y, f"NPR {row['price']}")

        y -= 20

        # Page break
        if y < 50:
            p.showPage()
            y = height - 50

    # ================= FINALIZE =================
    p.save()
    buffer.seek(0)
    return buffer