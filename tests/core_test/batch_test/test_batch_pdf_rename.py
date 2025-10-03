import os

from core.batch.batch_rename import batch_rename_pdfs


def test_batch_rename(pdfs_directory):
    """Successful batch rename of valid PDF files in a directory."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="some_base",
    )
    assert result.success is True


def test_batch_rename_explicit_output_directory(pdfs_directory, save_pdf_dir):
    """Successful batch rename specifying an explicit output directory."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="some_base",
        output_dir=save_pdf_dir,
    )
    assert result.success is True


def test_batch_rename_corrupt_pdfs(corrupt_pdfs_directory):
    """Fail batch rename when directory contains corrupt PDF files."""

    result = batch_rename_pdfs(
        input_dir=corrupt_pdfs_directory,
        base_name="some_base",
    )
    assert result.success is False


def test_batch_rename_nonexistent_directory():
    """Fail batch rename when input directory does not exist."""

    result = batch_rename_pdfs(
        input_dir="random_dir",
        base_name="some_base",
    )
    assert result.success is False


def test_batch_rename_empty_input_directory():
    """Fail batch rename when input directory path is empty."""

    result = batch_rename_pdfs(
        input_dir="",
        base_name="some_base",
    )
    assert result.success is False


def test_batch_rename_nonexistent_output_directory(pdfs_directory):
    """Fail batch rename when specified output directory does not exist."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory, base_name="some_base", output_dir="random_dir"
    )
    assert result.success is False


def test_batch_rename_no_base_name(pdfs_directory):
    """Fail batch rename when base name for renaming is empty."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="",
    )
    assert result.success is False


def test_batch_rename_incorrect_file(corrupt_pdfs_directory):
    """Fail batch rename when files with incorrect extensions are present."""

    result = batch_rename_pdfs(
        input_dir=corrupt_pdfs_directory,
        base_name="some_base",
    )
    assert result.success is False


def test_batch_rename_endswith_pdf(pdfs_directory):
    """Batch rename succeeds when base name ends with '.pdf'."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="some_base.pdf",
    )
    assert result.success is True


def test_batch_rename_long_base_name(pdfs_directory):
    """Batch rename succeeds with a very long base name."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="something_long_name_is_suggested_hence_I_am_writing_this_sentence_that_holds_no_meaning_of_its_own_yet_its_not_meaningless.pdf",
    )
    assert result.success is True


def test_batch_rename_with_dot_pdf_as_base_name(pdfs_directory):
    """Fail batch rename when base name is '.pdf' only."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name=".pdf",
    )
    assert result.success is False


def test_batch_rename_with_white_space_as_base_name(pdfs_directory):
    """Fail batch rename when base name is only whitespace."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name=" ",
    )
    assert result.success is False


def test_batch_rename_output_file_exists(pdfs_directory):
    """Fail batch rename if an output file with the new name already exists."""

    exists_pdf = os.listdir(pdfs_directory)[0]
    with open(os.path.join(pdfs_directory, exists_pdf), "w") as f:
        f.write("")

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name=f"{exists_pdf}_1",
    )
    assert result.success is False


def test_batch_rename_invalid_pdf(valid_invalid_pdfs):
    """Fail batch rename if directory contains invalid or corrupted PDFs."""

    input_directory = os.path.dirname(valid_invalid_pdfs[0])
    result = batch_rename_pdfs(input_dir=input_directory, base_name="some_name")
    assert result.success is False


def test_batch_rename_case_sensitive_base_name(pdfs_directory):
    """Batch rename succeeds with base name having uppercase '.PDF' extension."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="some_name.PDF",
    )
    assert result.success is True


def test_batch_rename_base_name_trailing_whitespace(pdfs_directory):
    """Batch rename succeeds when base name has trailing whitespace."""

    result = batch_rename_pdfs(
        input_dir=pdfs_directory,
        base_name="some_name   ",
    )
    assert result.success is True


def test_batch_rename_many_files(large_pdfs_directory):
    """Batch rename succeeds on directory containing many PDF files."""

    result = batch_rename_pdfs(
        input_dir=large_pdfs_directory,
        base_name="some_name",
    )
    assert result.success is True
