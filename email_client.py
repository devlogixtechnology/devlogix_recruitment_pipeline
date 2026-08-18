import imaplib
import ssl
import logging

from config import (
    GMAIL_ADDRESS,
    GMAIL_APP_PASSWORD,
    PROCESS_FROM_DATE,
)


IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

logger = logging.getLogger("recruitment_ingestion")


def connect_to_gmail():
    """
    Establish a secure IMAP connection to Gmail.
    """

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        raise ValueError(
            "Gmail credentials are not configured."
        )

    context = ssl.create_default_context()

    mail = imaplib.IMAP4_SSL(
        IMAP_SERVER,
        IMAP_PORT,
        ssl_context=context
    )

    mail.login(
        GMAIL_ADDRESS,
        GMAIL_APP_PASSWORD
    )

    logger.info("Successfully connected to Gmail.")

    return mail


def fetch_recent_emails(mail):
    """
    Fetch emails received from the configured processing date onward.
    """

    status, _ = mail.select("INBOX")

    if status != "OK":
        logger.error("Failed to open inbox.")
        return []

    gmail_date = PROCESS_FROM_DATE.strftime(
        "%d-%b-%Y"
    )

    search_criteria = f"SINCE {gmail_date}"

    status, messages = mail.search(
        None,
        search_criteria
    )

    if status != "OK":
        logger.error("Failed to search inbox.")
        return []

    email_ids = messages[0].split()

    logger.info(
        "Found %d email(s) since %s.",
        len(email_ids),
        gmail_date
    )

    return email_ids


def fetch_email(mail, email_id):
    """
    Fetch the complete raw email.
    """

    status, data = mail.fetch(
        email_id,
        "(RFC822)"
    )

    if status != "OK":
        logger.error(
            "Failed to fetch email %s.",
            email_id.decode(errors="ignore")
        )
        return None

    return data[0][1]


def close_connection(mail):
    """
    Close the Gmail connection safely.
    """

    try:
        mail.close()
    except Exception:
        pass

    try:
        mail.logout()
    except Exception:
        pass

    logger.info("Gmail connection closed.")