#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com


"""System modules"""
from os import listdir
from os.path import split, isfile, join

import pytest

# pylint: disable=import-error
from modules.cryptography.file_encryption import encrypt_file_name, encrypt_file_content


@pytest.mark.asyncio
async def test_encrypt_file_name(create_file, get_fernet):
    """
    This function test if a file name is successfully encrypted
    :param create_file: the file create by tmp_path
    :param get_fernet: the fernet instance with key loaded
    """
    await encrypt_file_name(create_file, get_fernet)
    path_to_file, __ = split(create_file)
    assert [join(f) for f in listdir(path_to_file) if isfile(join(path_to_file, f))] != ["test.txt"]


@pytest.mark.asyncio
async def test_encrypt_file_content(create_file, get_fernet):
    """
    This function test if a file content is successfully encrypted
    :param create_file: the file create by tmp_path
    :param get_fernet: the fernet instance with key loaded
    """
    old_content = create_file.open().read()
    await encrypt_file_content(create_file, get_fernet)
    assert old_content != create_file.open().read()
