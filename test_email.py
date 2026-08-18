from email.message import EmailMessage

from email_ingestion import process_email


def create_test_email():
    """
    Create a fake recruitment email for local testing.
    """

    email = EmailMessage()

    email["Subject"] = "Application for AI/ML Intern"
    email["From"] = "candidate@example.com"
    email["To"] = "recruitment@devlogix.com"
    email["Date"] = "Tue, 18 Aug 2026 17:00:00 +0500"
    email["Message-ID"] = "<test-candidate-001@devlogix.local>"

    email.set_content(
        "Hello,\n\n"
        "Please find my CV attached.\n\n"
        "Regards,\n"
        "Test Candidate"
    )

    email.add_attachment(
        b"This is a fake PDF CV for testing.",
        maintype="application",
        subtype="pdf",
        filename="Candidate_Test_CV.pdf"
    )

    return email


def main():
    print("=" * 50)
    print("RECRUITMENT EMAIL INGESTION TEST")
    print("=" * 50)

    test_email = create_test_email()

    raw_email = test_email.as_bytes()

    print("\nProcessing test email...\n")

    result = process_email(raw_email)

    print("\n" + "=" * 50)
    print(f"CVs processed: {result}")
    print("=" * 50)


if __name__ == "__main__":
    main()