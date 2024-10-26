from django.core.mail import send_mail
from django.conf import settings

def send_submission_status_email(user_email, form_title, status):
    subject = f'Submission Status Update: {form_title}'
    message = f'Your submission for "{form_title}" has been reviewed. The current status is: {status}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
