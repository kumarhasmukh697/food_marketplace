from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings



@shared_task
def send_otp_email(email, username, otp):
    send_mail(
        subject="Your OTP Verification Code",
        message=(
            f"Hello {username},\n\n"
            f"Your OTP is: {otp}\n\n"
            f"This OTP is valid for 10 minutes."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


# for running celery we have this below command
# celery -A config worker --pool=solo --loglevel=info