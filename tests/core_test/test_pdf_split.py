from core.pdf_splitter import split_pdf


def test_split(pdf_file_path, save_pdf_dir):
    """Successfully splits a valid PDF with multiple page ranges."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-3,4-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )

    assert result.success is True


def test_split_corrupt_pdf(corrupt_file, save_pdf_dir):
    """Fail split on corrupt PDF file."""

    result = split_pdf(
        file_path=corrupt_file,
        page_range_input="1-3,4-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_nonexistent_file(corrupt_file, save_pdf_dir):
    """Fail split when source file does not exist."""

    result = split_pdf(
        file_path=corrupt_file,
        page_range_input="1-3,4-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_no_new_name(pdf_file_path):
    """Fail split when no output directory is provided."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-3,4-5",
        output_dir="",
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_incorrect_file(save_pdf_dir):
    """Fail split when source file is not a PDF."""

    result = split_pdf(
        file_path="wrong.txt",
        page_range_input="1-3,4-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_file_exists(pdf_file_path):
    """Fail split when output path conflicts with the source file."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-3,4-5",
        output_dir=pdf_file_path,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_endswith_pdf(pdf_file_path, save_pdf_dir):
    """Split succeeds even if output filename ends with a .pdf."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-3,4-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is True


def test_split_invalid_page_range(pdf_file_path, save_pdf_dir):
    """Fail split with page range where start > end."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="3-1,4-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_single_page_format(pdf_file_path, save_pdf_dir):
    """Split succeeds when input includes single page numbers."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1,4,5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is True


def test_split_single_page_range(pdf_file_path, save_pdf_dir):
    """Split succeeds with single-page ranges like 1-1, 4-4."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-1,4-4,5-5",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is True


def test_split_large_pdf(large_pdf_file_path, save_pdf_dir):
    """Split succeeds on a large PDF with multiple non-continuous ranges."""

    result = split_pdf(
        file_path=large_pdf_file_path,
        page_range_input="1-5,8-12,15-20,25-75,99-111",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is True


def test_split_invalid_page_range_format(pdf_file_path, save_pdf_dir):
    """Fail split with page range in invalid format (e.g., '1-three')."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-three",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_empty_page_range(pdf_file_path, save_pdf_dir):
    """Fail split with empty or whitespace-only page range."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input=" ",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_out_of_bound_page_range(pdf_file_path, save_pdf_dir):
    """Fail split with page ranges that exceed total page count."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="1-1000 ",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False


def test_split_negative_page_range(pdf_file_path, save_pdf_dir):
    """Fail split with a negative page number in the range."""

    result = split_pdf(
        file_path=pdf_file_path,
        page_range_input="-1-3 ",
        output_dir=save_pdf_dir,
        ask_password_callback=None,
    )
    assert result.success is False
