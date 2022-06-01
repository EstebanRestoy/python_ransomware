#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""system modules"""
from os import rename
from os.path import split


def decrypt_file_content(path: str, fernet: object):
    """
    This function is used to decrypt the content of a file
    1) Open the file with read binary permission
    2) decrypt the content and put the clear content in :var decrypted_data
    3) Open the file with write binary permission and replace crypted_data with clear version

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    with open(path, "r+b") as file:
        decrypted_data = fernet.decrypt(file.read())
        file.seek(0)
        file.write(decrypted_data)
        file.truncate()


def decrypt_file_name(path: str, fernet: object):
    """
    This function is used to decrypt a file name
    1) we split the path given in param to have the base path and the crypted name of the file
    2) the file name is decrypted
    3) we used rename function from os to rename the file

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    path_to_file, file_name = split(path)
    name, extension = file_name.split(".")
    rename(path, path_to_file + '\\' + fernet.decrypt(name.encode()).decode() + "." + extension)


def decrypt_file(path: str, fernet: object):
    """
    This function is used to combine the 2 function above
    1) Call the decrypt file content function
    2) Call the decrypt file name function

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    try:
        decrypt_file_content(path, fernet)
        decrypt_file_name(path, fernet)
    except Exception as e:
        print("Error during decrypt file :" + path)
