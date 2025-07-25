import os


from core.batch.batch_split import batch_split_pdf


def test_batch_split(pdf_file_path):
    """Successfully split a valid PDF file into individual pages."""

    result = batch_split_pdf(file_path=pdf_file_path)
    assert result.success is True


def test_batch_split_explicit_output_directory(pdf_file_path, save_pdf_dir):
    """Successfully split a PDF file with an explicit output directory specified."""

    result = batch_split_pdf(file_path=pdf_file_path, output_dir=save_pdf_dir)
    assert result.success is True


def test_batch_split_corrupt_file(corrupt_file):
    """Fail to split a PDF when the file is corrupt or invalid."""

    result = batch_split_pdf(file_path=corrupt_file)
    assert result.success is False


def test_batch_split_nonexistent_file():
    """Fail to split when the provided PDF file path does not exist."""

    result = batch_split_pdf(file_path="nonexistent.pdf")
    assert result.success is False


def test_batch_split_incorrect_file():
    """Fail to split when the provided file is not a PDF (incorrect file type)."""

    result = batch_split_pdf(file_path="incorrect.txt")
    assert result.success is False


def test_batch_split_no_file():
    """Fail to split when no file path is provided (empty input)."""

    result = batch_split_pdf(file_path="")
    assert result.success is False


def test_batch_split_large_file(large_pdf_file_path):
    """Successfully split a large PDF file into individual pages."""

    result = batch_split_pdf(file_path=large_pdf_file_path)
    assert result.success is True


def test_batch_split_single_page_pdf(single_page_pdf):
    """Successfully split a single-page PDF file (edge case)."""

    result = batch_split_pdf(file_path=single_page_pdf)
    assert result.success is True


def test_batch_split_output_directory_nonexistent(pdf_file_path):
    """Fail to split when the specified output directory does not exist."""

    result = batch_split_pdf(file_path=pdf_file_path, output_dir="nonexistent/")
    assert result.success is False


def test_batch_split_wrong_output_directory(pdf_file_path):
    """Fail to split when the specified output directory is not a directory."""

    result = batch_split_pdf(file_path=pdf_file_path, output_dir="somefile.txt")
    assert result.success is False


def test_batch_split_file_exists(pdf_file_path):
    """Fail to split when the output file(s) already exist in the target directory."""

    exists_pdf = os.path.basename(pdf_file_path)
    exists_pdf_path = os.path.join(os.path.dirname(pdf_file_path), exists_pdf)

    with open(exists_pdf_path, "w") as f:
        f.write("")

    result = batch_split_pdf(file_path=pdf_file_path)
    assert result.success is False
