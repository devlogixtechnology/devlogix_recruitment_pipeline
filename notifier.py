import logging

import requests

from config import WEBHOOK_URL


logger = logging.getLogger("recruitment_ingestion")


def send_notification(message):
    """
    Send a notification through the configured webhook.
    """

    if not WEBHOOK_URL:
        logger.info(
            "Webhook not configured. Notification skipped."
        )
        return False

    payload = {
        "text": message
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        logger.info(
            "Notification sent successfully."
        )

        return True

    except requests.RequestException as error:

        logger.error(
            "Notification failed: %s",
            error
        )

        return False