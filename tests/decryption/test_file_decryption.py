#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""system modules"""
from os.path import split, exists

# pylint: disable=import-error
from modules.cryptography.file_decryption import decrypt_file_name, decrypt_file_content
from modules.cryptography.file_encryption import encrypt_file_name, encrypt_file_content


def test_decrypt_file_name(create_file, get_fernet):
    """
    This function test if a file name is successfully decrypted
    :param create_file: the file create by tmp_path
    :param get_fernet: the fernet instance with key loaded
    """
    path_to_file, file_name = split(create_file)
    encrypted_name = encrypt_file_name(create_file, get_fernet)
    decrypt_file_name(path_to_file + '/' + encrypted_name, get_fernet)
    assert exists(path_to_file + '/' + file_name)


def test_decrypt_file_content(create_file, get_fernet):
    """
    This function test if a file content is successfully decrypted
    :param create_file: the file create by tmp_path
    :param get_fernet: the fernet instance with key loaded
    """
    old_content = create_file.open().read()
    encrypt_file_content(create_file, get_fernet)
    decrypt_file_content(create_file, get_fernet)
    assert old_content == create_file.open().read()
