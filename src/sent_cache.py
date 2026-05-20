from src.sheet_writer import LOG_SHEET_TAB
from src.sheet_reader import get_google_sheet_client
from src.config_loader import config


def load_already_sent():
    client = get_google_sheet_client()
    spreadsheet = client.open(config.spreadsheet_name)
    try:
        worksheet = spreadsheet.worksheet(LOG_SHEET_TAB)
    except Exception:
        return set()
    records = worksheet.get_all_records()
    return {str(r["email"]).strip().lower() for r in records if r.get("email")}
