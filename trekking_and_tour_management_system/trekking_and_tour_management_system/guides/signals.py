from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from trekking_and_tour_management_system.guides.models import Guide


def generate_reset_link(user):
    token_generator = PasswordResetTokenGenerator()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    return f"http://127.0.0.1:8000/api/auth/password-reset-confirm/{uid}/{token}/"


@receiver(post_save, sender=Guide)
def send_guide_creation_email(sender, instance, created, **kwargs):
    print("🔥 Guide signals loaded")
    if not created:
        return

    user = instance.user
    user.must_change_password = True
    user.set_unusable_password()  
    user.save()

    reset_link = generate_reset_link(user)

    send_mail(
        subject="Your Guide Account is Ready",
        message=f"""
Hi {instance.full_name},

Your guide account has been created.

Set your password using this link:
{reset_link}

After setting password, you can log in using your email.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )