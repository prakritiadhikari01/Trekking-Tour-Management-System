from io import BytesIO

from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas

from trekking_and_tour_management_system.payments.models import Invoice, Payment


def render_invoice_pdf(payment: Payment, invoice: Invoice) -> bytes:
    booking = payment.booking
    package = booking.package
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColor(colors.HexColor("#0F172A"))
    pdf.rect(0, height - 90, width, 90, fill=True, stroke=False)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, height - 50, "TREKKING & TOUR")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 72, "Professional Travel Invoice")

    pdf.setFillColor(colors.HexColor("#111827"))
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(400, height - 130, "INVOICE")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(350, height - 150, f"Invoice ID: {invoice.invoice_id}")
    pdf.drawString(350, height - 168, f"Date: {payment.created_at.date()}")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 140, "Company Details")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 160, "Trekking & Tour Management System")
    pdf.drawString(50, height - 176, "Pokhara, Nepal")
    pdf.drawString(50, height - 192, "support@trekking.com")

    pdf.setFillColor(colors.HexColor("#F3F4F6"))
    pdf.roundRect(40, height - 340, 520, 95, 10, fill=True, stroke=False)
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(55, height - 275, "Customer Details")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(55, height - 295, f"Name: {booking.full_name}")
    pdf.drawString(55, height - 313, f"Email: {booking.email}")
    pdf.drawString(320, height - 295, f"Phone: {booking.phone_number}")
    pdf.drawString(320, height - 313, f"Trip: {booking.trip_start_date} to {booking.trip_end_date}")
    pdf.drawString(320, height - 331, f"Payment Ref: {payment.transaction_id or payment.pidx or 'N/A'}")

    table_data = [
        ["Package", "People", "Price", "Payment", "Booking"],
        [
            package.title,
            str(booking.number_of_people),
            f"NPR {payment.amount}",
            "Paid" if payment.status == "COMPLETED" else payment.status.title(),
            booking.booking_status.title(),
        ],
    ]
    table = Table(table_data, colWidths=[180, 70, 90, 90, 90])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 40, height - 470)

    pdf.setFillColor(colors.HexColor("#DCFCE7"))
    pdf.roundRect(350, height - 560, 190, 70, 10, fill=True, stroke=False)
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(370, height - 520, "TOTAL PAID")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(370, height - 545, f"NPR {payment.amount}")

    pdf.setStrokeColor(colors.HexColor("#CBD5E1"))
    pdf.line(40, 80, 550, 80)
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(170, 60, "Thank you for booking with us!")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(130, 45, f"Generated: {timezone.now():%Y-%m-%d %H:%M:%S UTC}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


def generate_or_update_invoice(payment_id: int) -> Invoice:
    payment = (
        Payment.objects.select_related("booking", "booking__package")
        .filter(id=payment_id, status="COMPLETED")
        .first()
    )
    if payment is None:
        raise ValueError("Payment not completed or does not exist.")

    booking = payment.booking
    invoice, _ = Invoice.objects.get_or_create(
        payment=payment,
        defaults={
            "booking": booking,
            "invoice_id": Invoice.build_invoice_id(payment.id),
            "access_token": Invoice.build_access_token(),
            "file": "",
        },
    )
    if not invoice.booking_id:
        invoice.booking = booking

    pdf_content = render_invoice_pdf(payment, invoice)
    filename = f"{invoice.invoice_id}.pdf"
    invoice.file.save(filename, ContentFile(pdf_content), save=False)
    invoice.save()
    return invoice
