from pathlib import Path
import re
import logging


ALLOWED_EXTENSIONS = {".pdf", ".docx"}

logger = logging.getLogger("recruitment_ingestion")


def clean_filename(filename):
    """
    Remove unsafe characters from a filename.
    """

    filename = Path(filename).name

    filename = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        filename
    )

    return filename


def is_cv_file(filename):
    """
    Check whether the file is a supported CV format.
    """

    if not filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


def save_attachment(filename, file_data):
    """
    Save a valid CV attachment to the downloads folder.
    """

    if not filename:
        logger.warning("Attachment has no filename.")
        return None

    if not is_cv_file(filename):
        logger.info(
            "Ignored unsupported attachment: %s",
            filename
        )
        return None

    if not file_data:
        logger.warning(
            "Attachment is empty: %s",
            filename
        )
        return None

    safe_filename = clean_filename(filename)

    if not safe_filename:
        logger.warning(
            "Invalid attachment filename: %s",
            filename
        )
        return None

    downloads_folder = Path("downloads")
    downloads_folder.mkdir(exist_ok=True)

    file_path = downloads_folder / safe_filename

    counter = 1

    while file_path.exists():

        name = Path(safe_filename).stem
        extension = Path(safe_filename).suffix

        new_filename = (
            f"{name}_{counter}{extension}"
        )

        file_path = downloads_folder / new_filename

        counter += 1

    with open(file_path, "wb") as file:
        file.write(file_data)

    logger.info(
        "CV saved locally: %s",
        file_path
    )

    return file_path