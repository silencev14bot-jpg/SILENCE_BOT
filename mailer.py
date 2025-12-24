import smtplib
from email.message import EmailMessage
import os

BOT_EMAIL = "silence.v1.4bot@gmail.com"
APP_PASSWORD = os.getenv("xvlq sibi ncqp svrd")  # safer

def send_mail(subject: str, body: str, to_email: str):
    msg = EmailMessage()
    msg["From"] = BOT_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(BOT_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)