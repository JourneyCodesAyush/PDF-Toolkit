import os

from core.pdf_merge import merge_pdf


def test_merge(multiple_pdfs, save_pdf_dir):
    """Successful merge of multiple valid PDF files."""

    result = merge_pdf(
        input_file_path=multiple_pdfs,
        output_file_path=os.path.join(save_pdf_dir, "sample.pdf"),
        ask_password_callback=None,
    )
    assert result.success is True


def test_merge_corrupt_pdf(corrupt_file, save_pdf_dir):
    """
    If all are invalid, fail merge operation.
    Successfully merge valid PDF files while storing the name of the invalid ones in Result object.
    """

    result = merge_pdf(
        input_file_path=corrupt_file,
        output_file_path=os.path.join(save_pdf_dir, "sample.pdf"),
        ask_password_callback=None,
    )
    assert result.success is False


def test_merge_nonexistent_file(save_pdf_dir):
    """Fail merge when input file does not exist."""

    result = merge_pdf(
        input_file_path=["non_existent"],
        output_file_path=os.path.join(save_pdf_dir, "sample.pdf"),
        ask_password_callback=None,
    )
    assert result.success is False


def test_merge_no_new_name(multiple_pdfs, save_pdf_dir):
    """Fail merge when output file name is empty."""

    result = merge_pdf(
        input_file_path=multiple_pdfs,
        output_file_path=os.path.join(save_pdf_dir, ""),
        ask_password_callback=None,
    )
    assert result.success is False


def test_merge_incorrect_file(save_pdf_dir):
    """
    If input PDFs are non-existent, fail merge.
    Merge valid PDFs and store the names of invalid ones in Result object.
    """

    result = merge_pdf(
        input_file_path=["wrong_file.txt"],
        output_file_path=os.path.join(save_pdf_dir, "sample.pdf"),
        ask_password_callback=None,
    )
    assert result.success is False


def test_merge_file_exists(multiple_pdfs, save_pdf_dir):
    """Fail merge when destination file already exists."""

    exists_pdf = os.path.basename(multiple_pdfs[0])

    exists_pdf_path = os.path.join(save_pdf_dir, exists_pdf)
    with open(exists_pdf_path, "w") as f:
        f.write("")

    result = merge_pdf(
        input_file_path=multiple_pdfs,
        output_file_path=exists_pdf_path,
        ask_password_callback=None,
    )
    assert result.success is False


def test_merge_long_name(multiple_pdfs, save_pdf_dir):
    """Merge succeeds with a very long output file name."""

    result = merge_pdf(
        input_file_path=multiple_pdfs,
        output_file_path=os.path.join(
            save_pdf_dir,
            "something_long_name_is_suggested_hence_I_am_writing_this_sentence_that_holds_no_meaning_of_its_own_yet_its_not_meaningless",
        ),
        ask_password_callback=None,
    )
    assert result.success is True


def test_merge_same_pdf(multiple_pdfs, save_pdf_dir):
    """Fail merge when output and input file are the same."""

    exists_pdf = multiple_pdfs[0]
    exists_pdf_path = os.path.join(save_pdf_dir, exists_pdf)

    result = merge_pdf(
        input_file_path=multiple_pdfs,
        output_file_path=exists_pdf_path,
        ask_password_callback=None,
    )
    assert result.success is False


def test_merge_fake_pdf_extension(save_pdf_dir):
    """
    Skip invalid or corrupt PDF files while merging and store in Result object, while successfully merging the valid ones.

    Fail merge when all files are invalid ones with just a .pdf extension.
    """

    fake_pdf = os.path.join(save_pdf_dir, "fake.pdf")
    with open(fake_pdf, "w") as f:
        f.write("I am not really a PDF!")

    result = merge_pdf(
        input_file_path=[fake_pdf],
        output_file_path=os.path.join(save_pdf_dir, "somename"),
        ask_password_callback=None,
    )

    assert result.success is False


def test_merge_mixed_valid_invalid(valid_invalid_pdfs, save_pdf_dir):
    """
    Skip invalid PDFs and successfully merge valid ones from a mix of valid and corrupt PDFs.
    """

    result = merge_pdf(
        input_file_path=valid_invalid_pdfs,
        output_file_path=os.path.join(save_pdf_dir, "merged.pdf"),
        ask_password_callback=None,
    )

    assert result.success is True


def test_merge_no_pdf(save_pdf_dir):
    """Fail merge when no input files are provided."""

    result = merge_pdf(
        input_file_path=[],
        output_file_path=os.path.join(save_pdf_dir, "somesample.pdf"),
        ask_password_callback=None,
    )

    assert result.success is False
