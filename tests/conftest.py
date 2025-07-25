import os
from tempfile import TemporaryDirectory

import pytest
from fpdf import FPDF

root_path = os.getcwd()


def create_pdf(save_location: str, page_nums: int = 7):
    """
    Generate a simple multi-page PDF file with sample content and save it to the given location.

    The PDF contains 5 pages, each with a title and several paragraphs of lorem ipsum text.

    Args:
        save_location (str): The file path where the generated PDF will be saved.
        page_nums (int): Number of pages the PDF shall have.
    """

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    lorem = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Suspendisse eget libero vitae justo blandit suscipit. "
        "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae. "
    )

    for i in range(1, page_nums):
        pdf.add_page()

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Page {i}: Sample Content", ln=True)

        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        for _ in range(3):
            pdf.multi_cell(0, 10, lorem)
            pdf.ln(3)

    pdf.output(save_location)


@pytest.fixture
def pdf_file_path():
    """Provide a temporary path to a valid sample PDF for testing purposes."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    temp_pdf = os.path.join(sample_dir.name, "tempfile1.pdf")
    create_pdf(temp_pdf, 10)

    try:
        yield temp_pdf
    finally:
        sample_dir.cleanup()


@pytest.fixture
def large_pdf_file_path():
    """Provide a temporary path to a valid, sample, and large PDF for testing purposes."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    temp_pdf = os.path.join(sample_dir.name, "tempfile1.pdf")
    create_pdf(temp_pdf, 113)

    try:
        yield temp_pdf
    finally:
        sample_dir.cleanup()


@pytest.fixture
def multiple_pdfs():
    """Provide a list of temporary file paths to multiple copies of a valid sample PDF for batch tests."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )
    input_pdfs_path = []
    for i in range(4):
        temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
        create_pdf(temp_pdf)
        input_pdfs_path.append(temp_pdf)

    try:
        yield input_pdfs_path
    finally:
        sample_dir.cleanup()


@pytest.fixture
def save_pdf_dir():
    """Provide a temporary directory path for saving generated PDF files during tests."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    try:
        yield sample_dir.name
    finally:
        sample_dir.cleanup()


@pytest.fixture
def corrupt_file():
    """Provide a temporary path to a corrupt PDF file (a text file named with .pdf extension) for negative test cases."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    temp_pdf = os.path.join(sample_dir.name, "tempfile1.pdf")

    with open(temp_pdf, "w") as f:
        f.write(
            "This is a .txt file with just a .pdf extension and hence can be called corrupt"
        )

    try:
        yield temp_pdf
    finally:
        sample_dir.cleanup()


@pytest.fixture
def valid_invalid_pdfs():
    """Provide a list of temporary file paths mixing valid and invalid PDF files for mixed input testing."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )
    input_pdfs_path = []
    for i in range(4):
        if i % 3 == 0:
            temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
            with open(temp_pdf, "w") as f:
                f.write("I am an invalid PDF!")
            input_pdfs_path.append(temp_pdf)
        else:
            temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
            create_pdf(temp_pdf)
            input_pdfs_path.append(temp_pdf)

    try:
        yield input_pdfs_path
    finally:
        sample_dir.cleanup()


@pytest.fixture
def pdfs_directory():
    """Provide a directory of temporary file paths to multiple copies of a valid sample PDF for positive batch tests."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    for i in range(4):
        temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
        create_pdf(temp_pdf)

    try:
        yield sample_dir.name
    finally:
        sample_dir.cleanup()


@pytest.fixture
def corrupt_pdfs_directory():
    """Provide a directory containing a mix of valid and invalid PDF files for batch merge testing."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    for i in range(4):
        if i % 3 == 0:
            temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
            with open(temp_pdf, "w") as f:
                f.write("I am an invalid PDF!")

        else:
            temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
            create_pdf(temp_pdf)

    try:
        yield sample_dir.name
    finally:
        sample_dir.cleanup()


@pytest.fixture
def large_pdfs_directory():
    """Provide a directory with multiple valid sample PDFs for large-scale batch testing."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    for i in range(111):
        temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
        create_pdf(temp_pdf)

    try:
        yield sample_dir.name
    finally:
        sample_dir.cleanup()


@pytest.fixture
def single_page_pdf():
    """Provide a temporary path to a valid, sample, and single-page PDF for testing purposes."""

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    temp_pdf = os.path.join(sample_dir.name, "tempfile1.pdf")
    create_pdf(temp_pdf, 1)

    try:
        yield temp_pdf
    finally:
        sample_dir.cleanup()

