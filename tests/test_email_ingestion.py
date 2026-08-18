from email.message import EmailMessage

from email_ingestion import (
    is_recruitment_email,
    is_recent_email,
    process_email,
)


def create_test_email(
    subject="Application for AI/ML Intern",
    message_id="<test-email@devlogix.local>",
    attachment=True,
):
    email = EmailMessage()

    email["Subject"] = subject
    email["From"] = "candidate@example.com"
    email["To"] = "recruitment@devlogix.com"
    email["Date"] = "Tue, 18 Aug 2026 17:00:00 +0500"
    email["Message-ID"] = message_id

    email.set_content("Test recruitment application.")

    if attachment:
        email.add_attachment(
            b"Test CV content",
            maintype="application",
            subtype="pdf",
            filename="Test_CV.pdf",
        )

    return email.as_bytes()


def test_recruitment_subject_is_detected():
    assert is_recruitment_email(
        "Application for AI/ML Intern"
    ) is True


def test_non_recruitment_subject_is_rejected():
    assert is_recruitment_email(
        "Company Newsletter"
    ) is False


def test_recent_email_is_detected():
    assert is_recent_email(
        "Tue, 18 Aug 2026 17:00:00 +0500"
    ) is True


def test_email_without_cv_processes_zero_files():
    raw_email = create_test_email(
        message_id="<no-cv-test@devlogix.local>",
        attachment=False,
    )

    result = process_email(raw_email)

    assert result == 0