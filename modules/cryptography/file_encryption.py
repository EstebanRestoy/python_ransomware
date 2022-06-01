#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""system modules"""
from os import rename
from os.path import split

def encrypt_file(path: str, fernet: object):
    """
    This function is used to combine the 2 function above
    1) Call the encrypt file content function
    2) Call the encrypt file name function

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    try:
        encrypt_file_content(path, fernet)
        encrypt_file_name(path, fernet)
    except Exception as exception:
        print("Error during encrypt file :" + path)
        print(exception)


def encrypt_file_content(path: str, fernet: object):
    """
    This function is used to encrypt the content of a file
    1) Open the file with read binary permission
    2) encrypt the content and put the encrypted content in :var encrypted_data
    3) Open the file with write binary permission and replace content with encrypted version

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    with open(path, "r+b") as file:
        encrypted_data = fernet.encrypt(file.read())
        file.seek(0)
        file.write(encrypted_data)
        file.truncate()


def encrypt_file_name(path: str, fernet: object):
    """
    This function is used to encrypt a file name
    1) we split the path given in param to have the base path and the name of the file
    2) the file name is encrypted and stored in :var encrypted_name
    3) we used rename function from os to rename the file

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    :return: the encrypted name of the file
    """
    path_to_file, file_name = split(path)
    name, extension = file_name.split(".")
    encrypted_name = fernet.encrypt(name.encode()).decode() + "." + extension
    rename(path, path_to_file + '/' + encrypted_name)
    return encrypted_name
