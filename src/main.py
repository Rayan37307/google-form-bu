import time
import traceback
import logging

from src.config_loader import config
from src.setup import needs_setup, run_setup
from src.sheet_reader import fetch_email_column
from src.email_checker import load_dataset_emails, find_matches
from src.email_sender import send_canva_invitation
from src.sheet_writer import log_sent_emails
from src.sent_cache import load_already_sent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def run_once():
    log.info("Checking Google Sheet for new emails...")

    try:
        sheet_emails = fetch_email_column()
    except Exception as e:
        log.error("Failed to fetch emails from sheet: %s\n%s", e, traceback.format_exc())
        return

    try:
        dataset_emails = load_dataset_emails()
    except Exception as e:
        log.error("Failed to load dataset: %s\n%s", e, traceback.format_exc())
        return

    try:
        already_sent = load_already_sent()
    except Exception as e:
        log.error("Failed to load sent cache: %s\n%s", e, traceback.format_exc())
        return

    to_send = find_matches(sheet_emails, dataset_emails, already_sent)

    if not to_send:
        log.info("No new matching emails found.")
        return

    sent = 0
    for email in to_send:
        try:
            send_canva_invitation(email)
            log_sent_emails([email])
            sent += 1
            log.info("Invitation sent to %s", email)
        except Exception as e:
            log.error("Failed to send/log for %s: %s\n%s", email, e, traceback.format_exc())

    log.info("Sent %d invitation(s).", sent)


def main():
    import sys

    if "--setup" in sys.argv:
        run_setup()
    elif needs_setup():
        run_setup()

    log.info("Starting Canva Pro invitation poller (interval=%ds)", config.poll_interval)
    while True:
        try:
            run_once()
        except Exception as e:
            log.error("Poll cycle failed: %s\n%s", e, traceback.format_exc())
        time.sleep(config.poll_interval)


if __name__ == "__main__":
    main()
