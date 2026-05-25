import secrets
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings




def generate_password():
    return secrets.token_urlsafe(10)

def send_application_received_email(application):

    message = f"""
Hi {application.full_name},

Your guide application has been received successfully.

We will review your application soon.
"""

    result = send_mail(
        subject="Guide Application Received",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[application.email],
    )
    print("Email sent:", result)

def create_guide_account(application):
    from trekking_and_tour_management_system.guides.models import Guide
    User = get_user_model()

    existing_user = User.objects.filter(
        email=application.email
    ).first()

    if existing_user:

        existing_user.role = "guide"
        existing_user.name = application.full_name
        existing_user.save()

        Guide.objects.get_or_create(
            user=existing_user,
            defaults={
                "full_name": application.full_name,
                "phone_number": application.phone_number,
                "experience": application.experience,
                "languages": application.languages,
                "created_from_application": application,
            }
        )
        send_mail(
            subject="Guide Access Approved",
            message=f"""
Hi {application.full_name},

Congratulations!

Your account has been approved as a Guide.

You can login using your existing password.

Login here:
http://127.0.0.1:8000/api/auth/login/
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[application.email],
        )

        return
    
    password = generate_password()

    user = User.objects.create_user(
        email=application.email,
        password=password,
        role="guide",
        name=application.full_name,

    )

    Guide.objects.create(
        user=user,
        full_name=application.full_name,
        phone_number=application.phone_number,
        experience=application.experience,
        languages=application.languages,
        created_from_application=application
    )

    send_guide_credentials(application, password)


def send_guide_credentials(application, password):
    login_url = "http://127.0.0.1:8000/api/auth/login/"

    message = f"""
Hi {application.full_name},

Congratulations! You are ACCEPTED as a Guide.

Your login credentials:

Username: {application.email}
Password: {password}

Login here: {login_url}

Please change your password after first login.
"""

    send_mail(
        subject="Guide Account Created",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[application.email],
    )


def send_status_email(application):
    if application.status == "ACCEPTED":
        message = f"Congratulations {application.full_name}, you are ACCEPTED."
    else:
        message = f"Sorry {application.full_name}, your application is REJECTED."

    send_mail(
        subject="Guide Application Status Update",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[application.email],
    )