from celery import Celery
from src.mail import create_message_new, send_email
from asgiref.sync import async_to_sync

c_app = Celery()

c_app.config_from_object('src.config')

@c_app.task()
def send_mail(email: str, subject: str, body: str):
    message = create_message_new(subject=subject)

    send_email(data=message, recipient_email=email, body=body)
    print("Email Sent")