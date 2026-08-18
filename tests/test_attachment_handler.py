from attachment_handler import (
    is_cv_file,
    clean_filename,
)


def test_pdf_is_allowed():
    assert is_cv_file("candidate.pdf") is True


def test_docx_is_allowed():
    assert is_cv_file("candidate.docx") is True


def test_jpg_is_rejected():
    assert is_cv_file("candidate.jpg") is False


def test_png_is_rejected():
    assert is_cv_file("candidate.png") is False


def test_filename_is_cleaned():
    result = clean_filename("../../candidate CV.pdf")

    assert result == "candidate_CV.pdf"