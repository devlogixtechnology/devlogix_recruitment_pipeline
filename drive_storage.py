from pathlib import Path
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]

CREDENTIALS_FILE = "credentials.json"

logger = logging.getLogger("recruitment_ingestion")


def connect_to_drive():
    """
    Connect to Google Drive using OAuth credentials.
    """

    credentials_path = Path(CREDENTIALS_FILE)

    if not credentials_path.exists():
        raise FileNotFoundError(
            "credentials.json not found. "
            "DevLogix must configure Google Drive authentication."
        )

    credentials = Credentials.from_authorized_user_file(
        str(credentials_path),
        SCOPES
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    logger.info(
        "Successfully connected to Google Drive."
    )

    return drive_service


def upload_file(drive_service, file_path, folder_id=None):
    """
    Upload a CV to Google Drive.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        logger.error(
            "File not found: %s",
            file_path
        )
        return None

    file_metadata = {
        "name": file_path.name
    }

    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(
        str(file_path),
        resumable=True
    )

    uploaded_file = (
        drive_service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id,name,webViewLink"
        )
        .execute()
    )

    logger.info(
        "Uploaded to Google Drive: %s",
        uploaded_file.get("name")
    )

    return uploaded_file