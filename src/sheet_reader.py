from src.auth import get_authenticated_client
from src.config_loader import config


def get_google_sheet_client():
    return get_authenticated_client()


def fetch_email_column():
    client = get_google_sheet_client()
    sheet = client.open(config.spreadsheet_name).worksheet(config.sheet_tab_name)
    records = sheet.get_all_records()
    emails = []
    for row in records:
        val = row.get(config.email_column_name, "")
        if val and str(val).strip():
            emails.append(str(val).strip().lower())
    return emails
