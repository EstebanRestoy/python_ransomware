#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import string
import random

import pytest
from cryptography.fernet import Fernet

FILE_TEXT = "I am the text file"
FILE_NAME = "test.txt"
DIRECTORY_PATH = "../sandbox"


def get_random_string(length):
    """
    This function return a random string
    1) Put all ascii letters lowercase in a var
    2) Use the random lib to take random letter from the array of letters
    3) return the result
    :param length: the length of the random string
    """
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@pytest.fixture()
def create_file(tmp_path):
    """
    This function create a file
    1) Create a directory with an random unique name
    2) Create a file in this directory
    3) Put the FILE_TEXT const data in the file
    :param tmp_path: the temporary path of the file
    """
    directory = tmp_path / get_random_string(8)
    directory.mkdir()
    file = directory / FILE_NAME
    file.write_text(FILE_TEXT)
    return file


@pytest.fixture()
def get_fernet():
    """
    This function return a Fernet object with a loaded key
    1) Generate a key
    2) Load Fernet with the key
    3) Return the Fernet instance
    """
    key = Fernet.generate_key()  # Generates the key
    fernet = Fernet(key)
    return fernet
