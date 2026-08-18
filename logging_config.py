import logging
from pathlib import Path


def setup_logging():
    """
    Configure application logging.
    """

    logs_folder = Path("logs")
    logs_folder.mkdir(exist_ok=True)

    log_file = logs_folder / "ingestion.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                log_file,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("recruitment_ingestion")