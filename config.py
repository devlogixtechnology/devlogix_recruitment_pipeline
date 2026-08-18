import os

from datetime import datetime

from dotenv import load_dotenv


load_dotenv()


GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


RECRUITMENT_KEYWORDS = [
    "application",
    "job application",
    "resume",
    "cv",
    "candidate",
]


PROCESS_FROM_DATE = datetime(
    2026,
    8,
    18
)