from src.config_loader import config
from src.sheet_reader import get_google_sheet_client


LOG_SHEET_TAB = "SentLog"


def ensure_log_sheet():
    client = get_google_sheet_client()
    spreadsheet = client.open(config.spreadsheet_name)
    try:
        worksheet = spreadsheet.worksheet(LOG_SHEET_TAB)
    except Exception:
        worksheet = spreadsheet.add_worksheet(title=LOG_SHEET_TAB, rows=1000, cols=3)
        worksheet.append_row(["email", "sent_at", "status"])
    return worksheet


def log_sent_emails(sent_emails):
    if not sent_emails:
        return
    from datetime import datetime, timezone

    worksheet = ensure_log_sheet()
    now = datetime.now(timezone.utc).isoformat()
    for email in sent_emails:
        worksheet.append_row([email, now, "sent"])
