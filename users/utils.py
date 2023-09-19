from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail


def send_confirmation_email(user):
    token = AccessToken.for_user(user)
    confirmation_url = f'http://127.0.0.1:8000/confirm-email/?token={token}'

    subject = 'Email Confirmation'
    message = f'Please confirm your registration by visiting the following link:\n\n{confirmation_url}'
    from_email = 'admin@ourapp.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
