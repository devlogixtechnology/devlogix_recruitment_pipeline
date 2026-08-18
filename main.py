from logging_config import setup_logging

from email_client import (
    connect_to_gmail,
    fetch_recent_emails,
    fetch_email,
    close_connection,
)

from email_ingestion import process_email


logger = setup_logging()


def main():
    """
    Main recruitment email ingestion workflow.
    """

    mail = None

    try:
        logger.info("Starting recruitment email ingestion.")

        mail = connect_to_gmail()

        email_ids = fetch_recent_emails(mail)

        logger.info(
            "Found %d email(s) to process.",
            len(email_ids)
        )

        for email_id in email_ids:

            logger.info(
                "Processing email: %s",
                email_id.decode()
            )

            raw_email = fetch_email(
                mail,
                email_id
            )

            if raw_email is None:
                logger.warning(
                    "Could not fetch email: %s",
                    email_id.decode()
                )
                continue

            try:
                process_email(raw_email)

            except Exception:
                logger.exception(
                    "Error processing email: %s",
                    email_id.decode()
                )

    except Exception:
        logger.exception(
            "Recruitment ingestion failed."
        )

    finally:
        if mail:
            close_connection(mail)

        logger.info(
            "Recruitment email ingestion finished."
        )


if __name__ == "__main__":
    main()