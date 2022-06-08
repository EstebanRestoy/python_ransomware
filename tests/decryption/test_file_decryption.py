#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""system modules"""
import glob
from os.path import split, exists, isfile

# pylint: disable=import-error

from modules.cryptography.file_decryption import decrypt_file_name, decrypt_file_content
from modules.cryptography.file_encryption import encrypt_file_name, encrypt_file_content


def get_all_files_in_directory(path):
    """
    This function return all files and sub_files in a directory passed in param
    1) Use Glob to get all the file and return them in array shape
    :param path: the start path
    """
    return [f for f in glob.glob(path + '/**/*',recursive=True) if isfile(f)]


def test_decrypt_file_name(create_file, get_fernet):
    """
    This function test if a file name is successfully decrypted
    :param create_file: the file create by tmp_path
    :param get_fernet: the fernet instance with key loaded
    """
    path_to_file, file_name = split(create_file)
    print(get_all_files_in_directory(path_to_file))
    encrypted_name = encrypt_file_name(create_file, get_fernet)
    print(get_all_files_in_directory(path_to_file))
    decrypt_file_name(path_to_file + '/' + encrypted_name, get_fernet)
    print(get_all_files_in_directory(path_to_file))

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
