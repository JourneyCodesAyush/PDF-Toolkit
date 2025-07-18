import os
import shutil
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture
def pdf_file_path():
    """Provide path to a valid sample PDF file for testing."""
    root_path = os.getcwd()

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    root_path = os.path.join(root_path, "SampleTesting")
    temp_pdf = os.path.join(sample_dir.name, "tempfile1.pdf")

    shutil.copy2(src=os.path.join(root_path, "sample_1.pdf"), dst=temp_pdf)

    yield temp_pdf
    sample_dir.cleanup()


@pytest.fixture
def multiple_pdfs():
    """Provide a list of paths to multiple copies of a sample PDF for batch testing."""
    root_path = os.getcwd()

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )
    input_pdfs_path = []
    for i in range(4):
        root_path = os.path.join(root_path, "SampleTesting")
        temp_pdf = os.path.join(sample_dir.name, f"tempfile{i}.pdf")
        shutil.copy2(
            src=os.path.join(root_path, "sample_1.pdf"), dst=f"tempfile{i}.pdf"
        )
        input_pdfs_path.append(temp_pdf)

    yield input_pdfs_path
    sample_dir.cleanup()


@pytest.fixture
def save_pdf_dir():
    """Provide a temporary directory path for saving PDF outputs during tests."""
    root_path = os.getcwd()
    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )
    yield sample_dir.name
    sample_dir.cleanup()


@pytest.fixture
def corrupt_file():
    """Provide path to a corrupt PDF file (a text file with .pdf extension) for negative testing."""
    root_path = os.getcwd()

    sample_dir = TemporaryDirectory(
        dir=os.path.join(root_path, "tests"), prefix="test_pdf_"
    )

    root_path = os.path.join(root_path, "SampleTesting")
    temp_pdf = os.path.join(sample_dir.name, "tempfile1.pdf")

    with open(temp_pdf, "w") as f:
        f.write(
            "This is a .txt file with just a .pdf extension and hence can be called corrupt"
        )

    yield temp_pdf
    sample_dir.cleanup()
