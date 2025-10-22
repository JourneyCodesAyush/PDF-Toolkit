# Global flags in the code are stored here

from enum import Enum, auto


class EncryptedFileHandling(Enum):
    """
    Enum to specify how encrypted PDF files should be handled in PDF operations.

    Members:
        - ASK: Prompt the user for a password to access the encrypted PDF.
        - SKIP: Skip the current encrypted PDF file without prompting.
        - SKIP_ALL: Skip all encrypted PDFs without prompting.

    This enum standardizes the app’s behavior when encountering encrypted PDFs,
    enabling consistent handling across features like merging or extracting pages.
    """

    ASK = auto()
    SKIP = auto()
    SKIP_ALL = auto()


ENCRYPTED_FILE_HANDLING = EncryptedFileHandling.ASK
