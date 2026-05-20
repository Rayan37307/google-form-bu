import csv

from src.config_loader import config


def load_dataset_emails():
    dataset_emails = set()
    with open(config.dataset_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = row.get(config.dataset_email_column, "")
            if val and str(val).strip():
                dataset_emails.add(str(val).strip().lower())
    return dataset_emails


def find_matches(sheet_emails, dataset_emails, already_sent):
    sheet_set = set(sheet_emails)
    eligible = sheet_set & dataset_emails
    return eligible - already_sent
