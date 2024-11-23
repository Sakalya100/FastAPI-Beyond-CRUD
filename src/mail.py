from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
)

mail = FastMail(
    config=mail_config
)

def create_message(recipients: list[str], subject: str,body: str):
    
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
    
    return message


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os


def create_message_new(subject: str):
    # Read sender details from environment variables
    sender_email = Config.MAIL_FROM
    sender_password = Config.MAIL_PASSWORD

    # Print statements to debug environment variables
    print(f"Sender Email: {sender_email}")
    print(f"Sender Password: {'***' if sender_password else None}")

    # Check if the environment variables are set
    if not sender_email or not sender_password:
        raise ValueError("SENDER_EMAIL and SENDER_PASSWORD environment variables must be set.")

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    print("EmailService initialized with SMTP server and port.")
    data = {
        "sender_email": sender_email,
        "sender_password": sender_password,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "subject": subject
    }
    return data

def send_email(data: dict, recipient_email, body: str, attachments=None):
    print(f"Preparing to send email to: {recipient_email}")
    print(f"Attachments: {attachments}")
    print(f"Sending Email from: {data}")
    
    smtp_server = data["smtp_server"]
    smtp_port = data["smtp_port"]
    sender_email = data["sender_email"]
    sender_password = data["sender_password"]
    subject = data["subject"]

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = data["sender_email"]
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'html'))
    print("Email body attached.")

    # Add attachments if any
    if attachments:
        try:
            with open(attachments, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype="txt")
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachments))
                msg.attach(attachment)
            print(f"Attachment {attachments} added.")
        except Exception as e:
            print(f"Failed to attach file {attachments}: {e}")

    try:
        # Create SMTP session        
        print("Creating SMTP session...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        print("SMTP session started with TLS.")

        # Login to the server
        print("Logging in to SMTP server...")
        server.login(sender_email, sender_password)
        print("Logged in successfully.")

        # Send email
        print("Sending email...")
        server.send_message(msg)
        print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        print("Closing SMTP session.")
        server.quit()