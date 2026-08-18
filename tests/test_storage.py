import json

import storage


def test_new_email_is_not_processed(tmp_path, monkeypatch):
    processed_file = tmp_path / "processed_emails.json"

    monkeypatch.setattr(
        storage,
        "PROCESSED_FILE",
        processed_file
    )

    assert storage.is_email_processed(
        "<new-email@devlogix.local>"
    ) is False


def test_saved_email_is_processed(tmp_path, monkeypatch):
    processed_file = tmp_path / "processed_emails.json"

    monkeypatch.setattr(
        storage,
        "PROCESSED_FILE",
        processed_file
    )

    email_id = "<processed-email@devlogix.local>"

    storage.save_processed_email(email_id)

    assert storage.is_email_processed(
        email_id
    ) is True


def test_processed_email_is_stored_once(tmp_path, monkeypatch):
    processed_file = tmp_path / "processed_emails.json"

    monkeypatch.setattr(
        storage,
        "PROCESSED_FILE",
        processed_file
    )

    email_id = "<duplicate-email@devlogix.local>"

    storage.save_processed_email(email_id)
    storage.save_processed_email(email_id)

    with open(
        processed_file,
        "r",
        encoding="utf-8"
    ) as file:
        processed = json.load(file)

    assert processed.count(email_id) == 1