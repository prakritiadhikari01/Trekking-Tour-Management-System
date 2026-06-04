from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


@shared_task
def send_guide_creation_email_task(user_id):
    user = User.objects.get(id=user_id)

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = PasswordResetTokenGenerator().make_token(
        user
    )

    reset_link = (
        f"{settings.APP_BASE_URL}"
        f"/api/auth/password-reset-confirm/"
        f"{uid}/{token}/"
    )

    send_mail(
        subject="Your Guide Account is Ready",
        message=f"""
Hi {user.name},

Your guide account has been created.

Set your password using this link:

{reset_link}

After setting password, you can log in using your email.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )

@shared_task
def test_task():
    print("CELERY WORKS")