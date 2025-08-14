from core.pdf_extract_pages import extract_pdf_page


def test_extract(pdf_file_path, save_pdf_dir):
    """Successfully splits a valid PDF with multiple page ranges."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="1-3,4-5", output_dir=save_pdf_dir
    )

    assert result.success is True


def test_extract_corrupt_pdf(corrupt_file, save_pdf_dir):
    """Fail extraction on corrupt PDF file."""

    result = extract_pdf_page(
        file_path=corrupt_file, page_range_input="1-3,4-5", output_dir=save_pdf_dir
    )
    assert result.success is False


def test_extract_nonexistent_file(corrupt_file, save_pdf_dir):
    """Fail extraction when source file does not exist."""

    result = extract_pdf_page(
        file_path=corrupt_file, page_range_input="1-3,4-5", output_dir=save_pdf_dir
    )
    assert result.success is False


def test_extract_no_new_name(pdf_file_path):
    """Fail extraction when no output directory is provided."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="1-3,4-5", output_dir=""
    )
    assert result.success is False


def test_extract_incorrect_file(save_pdf_dir):
    """Fail extraction when source file is not a PDF."""

    result = extract_pdf_page(
        file_path="wrong.txt", page_range_input="1-3,4-5", output_dir=save_pdf_dir
    )
    assert result.success is False


def test_extract_file_exists(pdf_file_path):
    """Fail extraction when output path conflicts with the source file."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="1-3,4-5", output_dir=pdf_file_path
    )
    assert result.success is False


def test_extract_endswith_pdf(pdf_file_path, save_pdf_dir):
    """Extraction succeeds even if output filename ends with a .pdf."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="1-3,4-5", output_dir=save_pdf_dir
    )
    assert result.success is True


def test_extract_invalid_page_range(pdf_file_path, save_pdf_dir):
    """Fail extraction with page range where start > end."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="3-1,4-5", output_dir=save_pdf_dir
    )
    assert result.success is False


def test_extract_single_page_format(pdf_file_path, save_pdf_dir):
    """Extraction succeeds when input includes single page numbers."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="1,4,5", output_dir=save_pdf_dir
    )
    assert result.success is True


def test_extract_single_page_range(pdf_file_path, save_pdf_dir):
    """Extraction succeeds with single-page ranges like 1-1, 4-4."""

    result = extract_pdf_page(
        file_path=pdf_file_path, page_range_input="1-1,4-4,5-5", output_dir=save_pdf_dir
    )
    assert result.success is True


def test_extract_large_pdf(large_pdf_file_path, save_pdf_dir):
    """Extraction succeeds on a large PDF with multiple non-continuous ranges."""

    result = extract_pdf_page(
        file_path=large_pdf_file_path,
        page_range_input="1-5,8-12,15-20,25-75,99-111",
        output_dir=save_pdf_dir,
    )
    assert result.success is True


def test_extract_invalid_page_range_format(pdf_file_path, save_pdf_dir):
    """Fail extraction with page range in invalid format (e.g., '1-three')."""

    result = extract_pdf_page(
        file_path=pdf_file_path,
        page_range_input="1-three",
        output_dir=save_pdf_dir,
    )
    assert result.success is False


def test_extract_empty_page_range(pdf_file_path, save_pdf_dir):
    """Fail extraction with empty or whitespace-only page range."""

    result = extract_pdf_page(
        file_path=pdf_file_path,
        page_range_input=" ",
        output_dir=save_pdf_dir,
    )
    assert result.success is False


def test_extract_out_of_bound_page_range(pdf_file_path, save_pdf_dir):
    """Fail extraction with page ranges that exceed total page count."""

    result = extract_pdf_page(
        file_path=pdf_file_path,
        page_range_input="1-1000 ",
        output_dir=save_pdf_dir,
    )
    assert result.success is False


def test_extract_negative_page_range(pdf_file_path, save_pdf_dir):
    """Fail extraction with a negative page number in the range."""

    result = extract_pdf_page(
        file_path=pdf_file_path,
        page_range_input="-1-3 ",
        output_dir=save_pdf_dir,
    )
    assert result.success is False
