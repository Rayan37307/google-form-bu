import smtplib
from email.mime.text import MIMEText

from src.config_loader import config


def send_canva_invitation(recipient_email):
    msg = MIMEText(config.email_body, "plain", "utf-8")
    msg["Subject"] = config.email_subject
    msg["From"] = config.email_sender
    msg["To"] = recipient_email

    with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
        server.starttls()
        if config.email_password:
            server.login(config.email_sender, config.email_password)
        server.send_message(msg)
