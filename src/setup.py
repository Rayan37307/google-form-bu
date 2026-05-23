import os
import logging
from pathlib import Path

from src.auth import get_authenticated_client

log = logging.getLogger(__name__)

ENV_PATH = Path(__file__).parent.parent / ".env"


def _list_spreadsheets(client):
    files = client.openall()
    return [s for s in files if s]


def _pick_spreadsheet(client):
    sheets = _list_spreadsheets(client)
    if not sheets:
        print("No Google Sheets found in your account.")
        return None
    print("\n--- Select a Google Sheet ---")
    for i, s in enumerate(sheets, 1):
        print(f"  {i}. {s.title}")
    while True:
        try:
            choice = input(f"\nEnter number (1-{len(sheets)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(sheets):
                return sheets[idx]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def _pick_worksheet(spreadsheet):
    worksheets = spreadsheet.worksheets()
    if not worksheets:
        print("No worksheets found in this spreadsheet.")
        return None
    print(f"\n--- Select a worksheet in '{spreadsheet.title}' ---")
    for i, ws in enumerate(worksheets, 1):
        print(f"  {i}. {ws.title}")
    while True:
        try:
            choice = input(f"\nEnter number (1-{len(worksheets)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(worksheets):
                return worksheets[idx]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def _pick_column(worksheet):
    headers = worksheet.row_values(1)
    if not headers:
        print("No headers found in the first row.")
        return None
    print(f"\n--- Select the column containing emails in '{worksheet.title}' ---")
    for i, h in enumerate(headers, 1):
        print(f"  {i}. {h}")
    while True:
        try:
            choice = input(f"\nEnter number (1-{len(headers)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(headers):
                return headers[idx]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def _pick_dataset():
    print("\n--- Dataset CSV ---")
    default = os.getenv("DATASET_PATH", "config/email1.csv")
    path = input(f"Path to dataset CSV (default: {default}): ").strip()
    return path or default


def _save_config(sheet_name, tab_name, column_name, dataset_path):
    lines = []
    found_keys = set()
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("SPREADSHEET_NAME="):
                    lines.append(f"SPREADSHEET_NAME={sheet_name}\n")
                    found_keys.add("SPREADSHEET_NAME")
                elif stripped.startswith("SHEET_TAB_NAME="):
                    lines.append(f"SHEET_TAB_NAME={tab_name}\n")
                    found_keys.add("SHEET_TAB_NAME")
                elif stripped.startswith("EMAIL_COLUMN_NAME="):
                    lines.append(f"EMAIL_COLUMN_NAME={column_name}\n")
                    found_keys.add("EMAIL_COLUMN_NAME")
                elif stripped.startswith("DATASET_PATH="):
                    lines.append(f"DATASET_PATH={dataset_path}\n")
                    found_keys.add("DATASET_PATH")
                else:
                    lines.append(line)

    if "SPREADSHEET_NAME" not in found_keys:
        lines.append(f"SPREADSHEET_NAME={sheet_name}\n")
    if "SHEET_TAB_NAME" not in found_keys:
        lines.append(f"SHEET_TAB_NAME={tab_name}\n")
    if "EMAIL_COLUMN_NAME" not in found_keys:
        lines.append(f"EMAIL_COLUMN_NAME={column_name}\n")
    if "DATASET_PATH" not in found_keys:
        lines.append(f"DATASET_PATH={dataset_path}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    log.info("Configuration saved to .env")


def needs_setup():
    spreadsheet = os.getenv("SPREADSHEET_NAME", "")
    tab = os.getenv("SHEET_TAB_NAME", "")
    column = os.getenv("EMAIL_COLUMN_NAME", "")
    return not spreadsheet or not tab or not column


def run_setup():
    print("\n=== Google Form Bu - Interactive Setup ===\n")
    client = get_authenticated_client()
    spreadsheet = _pick_spreadsheet(client)
    if not spreadsheet:
        return False
    worksheet = _pick_worksheet(spreadsheet)
    if not worksheet:
        return False
    column = _pick_column(worksheet)
    if not column:
        return False
    dataset_path = _pick_dataset()
    _save_config(spreadsheet.title, worksheet.title, column, dataset_path)
    print("\nSetup complete! The app will now start.\n")
    return True
