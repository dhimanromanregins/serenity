import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(user, otp):
    subject = 'Your OTP Code'
    message = render_to_string('Authentication/otp_email.html', {
        'user': user,
        'otp': otp,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
