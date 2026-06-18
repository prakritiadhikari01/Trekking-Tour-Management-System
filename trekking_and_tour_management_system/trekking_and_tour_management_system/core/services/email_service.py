from django.conf import settings
from django.core.mail import send_mail


class EmailService:
    """
    Central email gateway.

    Only this class should directly use Django's send_mail.
    """

    @staticmethod
    def send_plain_email(
        *,
        subject: str,
        message: str,
        recipient_list: list[str],
        fail_silently: bool = False,
    ) -> None:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
        )