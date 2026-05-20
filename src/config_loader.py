import os
import yaml
from dotenv import load_dotenv


load_dotenv()


class Config:
    def __init__(self):
        self.google_credentials_path = os.getenv("GOOGLE_SHEET_CREDENTIALS_PATH", "config/google-credentials.json")
        self.spreadsheet_name = os.getenv("SPREADSHEET_NAME", "")
        self.sheet_tab_name = os.getenv("SHEET_TAB_NAME", "Sheet1")
        self.email_column_name = os.getenv("EMAIL_COLUMN_NAME", "email")

        self.dataset_path = os.getenv("DATASET_PATH", "config/dataset.csv")
        self.dataset_email_column = os.getenv("DATASET_EMAIL_COLUMN", "email")

        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_sender = os.getenv("EMAIL_SENDER", "")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")

        self.email_subject = os.getenv("EMAIL_SUBJECT", "You're invited to Canva Pro!")
        self.email_body = os.getenv("EMAIL_BODY", "Hi, you've been invited to join Canva Pro.")

        self.poll_interval = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))


config = Config()
