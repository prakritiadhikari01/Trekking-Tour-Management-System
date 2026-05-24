from django.core.mail import send_mail


def send_application_status_email(application):
    subject = "Guide Application Status Update"

    if application.status == "ACCEPTED":
        message = f"""
Hi {application.full_name},

Congratulations! Your guide application has been ACCEPTED.

We will contact you soon.

Thanks,
Trekking Team
"""
    elif application.status == "REJECTED":
        message = f"""
Hi {application.full_name},

We regret to inform you that your guide application has been REJECTED.

You may apply again in the future.

Thanks,
Trekking Team
"""
    else:
        return

    send_mail(
        subject,
        message,
        "your_email@gmail.com",
        [application.email],
        fail_silently=False
    )