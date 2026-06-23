from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template.loader import render_to_string


def _admin_emails() -> list[str]:
    admin_emails: list[str] = []
    for admin in getattr(settings, "ADMINS", []):
        if isinstance(admin, (list, tuple)) and len(admin) > 1:
            admin_emails.append(admin[1])
        elif isinstance(admin, str) and "@" in admin:
            admin_emails.append(admin)
    configured = getattr(settings, "BOOKING_ADMIN_EMAILS", [])
    admin_emails.extend(configured if isinstance(configured, list) else [])
    return sorted({email for email in admin_emails if email})


def send_html_email(
    *,
    subject: str,
    template_name: str,
    context: dict,
    recipients: list[str],
) -> None:
    if not recipients:
        return

    html_content = render_to_string(template_name, context)
    text_content = render_to_string("emails/base.txt", context)

    connection = get_connection(fail_silently=False)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
        connection=connection,   # 🔥 IMPORTANT FIX
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

def send_event_emails(
    *,
    user_subject: str,
    admin_subject: str,
    user_template: str,
    admin_template: str,
    context: dict,
    user_email: str | None,
) -> None:
    if user_email:
        send_html_email(
            subject=user_subject,
            template_name=user_template,
            context=context,
            recipients=[user_email],
        )
    send_html_email(
        subject=admin_subject,
        template_name=admin_template,
        context=context,
        recipients=_admin_emails(),
    )

def send_refund_request_email(refund, booking, refund_amount, refund_percentage):
    send_mail(
        subject="Refund Request",
        message=f"""
Refund Request

Booking ID: {booking.id}
Customer: {booking.user.email}

Refund Amount: Rs {refund_amount}
Refund Percentage: {refund_percentage}%

Payment Method: {refund.payment_method}
Refund Account: {refund.refund_account}
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["admin@example.com"]
    )