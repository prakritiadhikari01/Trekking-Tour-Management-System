from core.services.email_service import EmailService


class GuideNotificationService:

    @staticmethod
    def send_account_ready_email(
        *,
        user,
        reset_link: str,
    ):
        message = f"""
Hi {user.name},

Your guide account has been created.

Set your password using the link below:

{reset_link}

After setting your password,
you can log in using your email.
"""

        EmailService.send_plain_email(
            subject="Your Guide Account Is Ready",
            message=message,
            recipient_list=[user.email],
        )