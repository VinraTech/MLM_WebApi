
from django.core.mail import send_mail
from django.conf import settings


def send_forgot_password_mail(email,otp):
    subject = 'Forgot password email'
    message = f'Hi, The OTP to reset your password is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject, message, email_from, recipient_list)
    return True