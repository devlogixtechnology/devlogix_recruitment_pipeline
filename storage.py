import json
from pathlib import Path


PROCESSED_FILE = Path("processed_emails.json")


def load_processed_emails():
    """
    Load the list of already processed email IDs.
    """

    if not PROCESSED_FILE.exists():
        return set()

    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data)

    except (json.JSONDecodeError, OSError):
        return set()


def save_processed_email(email_id):
    """
    Add an email ID to the processed list.
    """

    processed_emails = load_processed_emails()

    processed_emails.add(email_id)

    with open(PROCESSED_FILE, "w", encoding="utf-8") as file:
        json.dump(
            list(processed_emails),
            file,
            indent=4
        )


def is_email_processed(email_id):
    """
    Check whether an email has already been processed.
    """

    processed_emails = load_processed_emails()

    return email_id in processed_emails