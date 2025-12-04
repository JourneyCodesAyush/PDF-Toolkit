import os

from core.batch.batch_merge import batch_merge_pdfs


def test_batch_merge(pdfs_directory):
    """Successfully merge multiple valid PDF files in a directory."""

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name="some_name",
        output_dir=pdfs_directory,
        ask_password_callback=None,
    )
    assert result.success is True


def test_batch_merge_corrupt_pdf(corrupt_pdfs_directory):
    """
    Successfully batch merge valid PDFs when directory contains corrupt PDF files and store them in Result object.
    """

    result = batch_merge_pdfs(
        input_dir_path=corrupt_pdfs_directory,
        new_name="some_name",
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is True


def test_batch_merge_no_directory():
    """Fail batch merge when input directory path is empty."""

    result = batch_merge_pdfs(
        input_dir_path="",
        new_name="random_name",
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is False


def test_batch_merge_no_new_name(pdfs_directory):
    """Fail batch merge when no output file name is provided."""

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name="",
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is False


def test_batch_merge_incorrect_directory():
    """Fail batch merge when input directory does not exist or is invalid."""

    result = batch_merge_pdfs(
        input_dir_path="ProjectPDF/assets",
        new_name="",
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is False


def test_batch_merge_file_exists(pdfs_directory):
    """Fail batch merge when output file name already exists in directory."""

    exists_pdf = os.listdir(pdfs_directory)[0]

    exists_pdf_path = os.path.join(pdfs_directory, exists_pdf)
    with open(exists_pdf_path, "w") as f:
        f.write("")

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name=exists_pdf,
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is False


def test_batch_merge_long_name(pdfs_directory):
    """Successfully merge with a very long output file name."""

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name="something_long_name_is_suggested_hence_I_am_writing_this_sentence_that_holds_no_meaning_of_its_own_yet_its_not_meaningless",
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is True


def test_batch_merge_nonexistent_output_directory(pdfs_directory):
    """Fail batch merge when the specified output directory does not exist."""

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name="some_random_name",
        output_dir="does_not_exist",
        ask_password_callback=None,
    )

    assert result.success is False


def test_batch_merge_fake_pdf_extension(corrupt_pdfs_directory):
    """
    Successfully batch merge valid PDFs when directory contains non-PDF file with .pdf extension.
    """

    fake_pdf = os.path.join(corrupt_pdfs_directory, "fake.txt")

    with open(fake_pdf, "w") as f:
        f.write("I am not really a PDF!")

    result = batch_merge_pdfs(
        input_dir_path=corrupt_pdfs_directory,
        new_name="random_pdf",
        output_dir=None,
        ask_password_callback=None,
    )
    assert result.success is True


def test_batch_merge_output_location(pdfs_directory, save_pdf_dir):
    """Successfully save merged output in a custom output directory."""

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name="batch_merged_pdf",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )

    assert result.success is True


def test_batch_merge_large_directory(large_pdfs_directory):
    """Successfully merge a large number of PDF files."""

    result = batch_merge_pdfs(
        input_dir_path=large_pdfs_directory,
        new_name="batch_merged_pdf",
        output_dir=None,
        ask_password_callback=None,
    )

    assert result.success is True


def test_batch_merge_output_name_matches_input_file(pdfs_directory):
    """Fail batch merge when output file name matches an input file name."""

    first_pdf = os.listdir(pdfs_directory)[0]

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name=first_pdf,
        output_dir=None,
        ask_password_callback=None,
    )
    assert result.success is False


def test_batch_merge_with_non_pdf_file_in_dir(pdfs_directory):
    """Successfully merge PDFs even when some non-PDF files exist in the directory."""

    with open(os.path.join(os.path.abspath(pdfs_directory), "random.txt"), "w") as f:
        f.write("I am just a random text file!")

    result = batch_merge_pdfs(
        input_dir_path=pdfs_directory,
        new_name="batch_merge_pdf",
        output_dir=None,
        ask_password_callback=None,
    )
    assert result.success is True
