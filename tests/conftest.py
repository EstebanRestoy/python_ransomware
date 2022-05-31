import string
import random

import pytest
from cryptography.fernet import Fernet

FILE_TEXT = "I am the text file"
FILE_NAME = "test.txt"
DIRECTORY_PATH = "../sandbox"


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@pytest.fixture()
def create_file(tmp_path):
    d = tmp_path / get_random_string(8)
    d.mkdir()
    p = d / FILE_NAME
    p.write_text(FILE_TEXT)
    return p


@pytest.fixture()
def get_fernet(tmp_path):
    key = Fernet.generate_key()  # Generates the key
    fernet = Fernet(key)
    return fernet
