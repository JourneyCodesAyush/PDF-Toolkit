from core.pdf_rename import rename_pdf_file


def test_rename_pdf(pdf_file_path, save_pdf_dir):
    """Successful rename of a valid PDF file."""
    result = rename_pdf_file(
        old_path=pdf_file_path, new_directory=save_pdf_dir, new_name="something"
    )
    assert result.success is True


def test_rename_corrupt_pdf(corrupt_file, save_pdf_dir):
    """Fail rename on corrupt PDF file."""
    result = rename_pdf_file(
        old_path=corrupt_file, new_directory=save_pdf_dir, new_name="something"
    )
    assert result.success is False


def test_rename_nonexistent_file(save_pdf_dir):
    """Fail rename when source file does not exist."""
    result = rename_pdf_file(
        old_path="non_existent", new_directory=save_pdf_dir, new_name="something"
    )
    assert result.success is False


def test_rename_no_new_name(pdf_file_path, save_pdf_dir):
    """Fail rename when new file name is empty."""
    result = rename_pdf_file(
        old_path=pdf_file_path, new_directory=save_pdf_dir, new_name=""
    )
    assert result.success is False


def test_rename_incorrect_file(save_pdf_dir):
    """Fail rename when source file has wrong extension."""
    result = rename_pdf_file(
        old_path="something.txt", new_directory=save_pdf_dir, new_name="sample"
    )
    assert result.success is False


def test_rename_file_exists(pdf_file_path, save_pdf_dir):
    """Fail rename when destination file already exists."""
    result = rename_pdf_file(
        old_path=pdf_file_path, new_directory=save_pdf_dir, new_name=pdf_file_path
    )
    assert result.success is False


def test_rename_endswith_pdf(pdf_file_path, save_pdf_dir):
    """Rename succeeds when name ends in a .pdf."""
    result = rename_pdf_file(
        old_path=pdf_file_path, new_directory=save_pdf_dir, new_name="something.pdf"
    )
    assert result.success is True


def test_rename_same_pdf(pdf_file_path, save_pdf_dir):
    """Fail rename when new name is the same as original."""
    result = rename_pdf_file(
        old_path=pdf_file_path, new_directory=save_pdf_dir, new_name=pdf_file_path
    )
    assert result.success is False


def test_rename_long_name(pdf_file_path, save_pdf_dir):
    """Rename succeeds with a very long new file name."""
    result = rename_pdf_file(
        old_path=pdf_file_path,
        new_directory=save_pdf_dir,
        new_name="something_long_name_is_suggested_hence_I_am_writing_this_sentence_that_holds_no_meaning_of_its_own_yet_its_not_meaningless",
    )
    assert result.success is True
