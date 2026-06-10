from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from datetime import datetime


def generate_booking_revenue_pdf(bookings, revenue, start_date=None, end_date=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # ================= HEADER =================
    title = Paragraph("<b>BOOKING & REVENUE REPORT</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 10))

    generated = Paragraph(
        f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    )
    elements.append(generated)
    elements.append(Spacer(1, 10))

    if start_date and end_date:
        period = Paragraph(
            f"<b>Period:</b> {start_date} to {end_date}",
            styles["Normal"]
        )
        elements.append(period)
        elements.append(Spacer(1, 15))

    # ================= SUMMARY =================
    summary = Paragraph(
        f"<b>Total Revenue:</b> NPR {revenue}",
        styles["Heading2"]
    )
    elements.append(summary)
    elements.append(Spacer(1, 15))

    # ================= TABLE =================
    data = [["Booking ID", "User", "Price"]]

    for b in bookings:
        data.append([
            str(b.id),
            str(b.user),
            f"NPR {b.package.price}"
        ])

    table = Table(data, colWidths=[100, 250, 100])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)

    # ================= BUILD =================
    doc.build(elements)
    buffer.seek(0)
    return buffer