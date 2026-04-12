import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(subject, body):
    sender = os.getenv("GMAIL_SENDER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("GMAIL_TO")

    if not sender or not app_password or not to_email:
        print("❌ Missing Gmail email settings in .env")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Gmail send error:", e)