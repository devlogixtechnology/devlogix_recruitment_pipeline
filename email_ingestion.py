from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
import logging

from storage import (
    is_email_processed,
    save_processed_email
)

from config import (
    RECRUITMENT_KEYWORDS,
    PROCESS_FROM_DATE
)

from attachment_handler import save_attachment
from drive_storage import (
    connect_to_drive,
    upload_file
)

from notifier import send_notification


logger = logging.getLogger("recruitment_ingestion")


def is_recent_email(date_string):
    """
    Check whether an email is newer than the configured date.
    """

    if not date_string:
        return False

    try:
        email_date = parsedate_to_datetime(
            date_string
        )

        email_date = email_date.replace(
            tzinfo=None
        )

        return email_date >= PROCESS_FROM_DATE

    except (TypeError, ValueError):
        logger.warning(
            "Invalid email date: %s",
            date_string
        )
        return False


def is_recruitment_email(subject):
    """
    Check whether an email subject appears
    to be related to recruitment.
    """

    if not subject:
        return False

    subject = subject.lower()

    return any(
        keyword.lower() in subject
        for keyword in RECRUITMENT_KEYWORDS
    )


def process_email(raw_email):
    """
    Parse an email and process its CV attachments.
    """

    message = BytesParser(
        policy=policy.default
    ).parsebytes(raw_email)

    subject = message["subject"]
    sender = message["from"]
    date = message["date"]
    email_id = message["Message-ID"]

    logger.info(
        "Email received | Subject: %s | From: %s",
        subject,
        sender
    )

    if not email_id:
        logger.warning(
            "Email has no Message-ID. Ignoring."
        )
        return 0

    if is_email_processed(email_id):
        logger.info(
            "Email already processed. Ignoring."
        )
        return 0

    if not is_recent_email(date):
        logger.info(
            "Email is too old. Ignoring."
        )
        return 0

    if not is_recruitment_email(subject):
        logger.info(
            "Not a recruitment email. Ignoring."
        )
        return 0

    logger.info(
        "Recruitment email detected."
    )

    drive_service = None

    try:
        drive_service = connect_to_drive()

        logger.info(
            "Google Drive connection successful."
        )

    except FileNotFoundError:
        logger.info(
            "Google Drive not configured. "
            "Saving CV locally only."
        )

    except Exception as error:
        logger.warning(
            "Google Drive connection failed: %s",
            error
        )

    attachment_count = 0

    for part in message.walk():

        if part.get_content_disposition() != "attachment":
            continue

        filename = part.get_filename()

        if not filename:
            continue

        file_data = part.get_payload(
            decode=True
        )

        if not file_data:
            continue

        saved_file = save_attachment(
            filename,
            file_data
        )

        if not saved_file:
            continue

        attachment_count += 1

        logger.info(
            "Processed CV: %s",
            saved_file
        )

        if drive_service:

            try:
                upload_file(
                    drive_service,
                    saved_file
                )

                logger.info(
                    "Uploaded CV to Google Drive: %s",
                    saved_file
                )

            except Exception as error:

                logger.error(
                    "Google Drive upload failed: %s",
                    error
                )

    logger.info(
        "CVs processed: %d",
        attachment_count
    )

    if attachment_count > 0:

        save_processed_email(
            email_id
        )

        logger.info(
            "Email marked as processed."
        )

        try:

            send_notification(
                f"New recruitment application processed. "
                f"{attachment_count} CV(s) saved."
            )

        except Exception as error:

            logger.warning(
                "Notification failed: %s",
                error
            )

    return attachment_count