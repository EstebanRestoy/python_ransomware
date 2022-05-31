#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""asyncio module for async await"""
import asyncio
from os import rename
from os.path import split


async def decrypt_file_content(path: str, fernet: object):
    """
    This function is used to decrypt the content of a file
    1) Open the file with read binary permission
    2) decrypt the content and put the clear content in :var decrypted_data
    3) Open the file with write binary permission and replace crypted_data with clear version

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    with open(path, "rb") as file:
        file_data = file.read()

    decrypted_data = fernet.decrypt(file_data)

    with open(path, "wb") as file:
        file.write(decrypted_data)


async def decrypt_file_name(path: str, fernet: object):
    """
    This function is used to encrypt a file name
    1) we split the path given in param to have the base path and the crypted name of the file
    2) the file name is decrypted
    3) we used rename function from os to rename the file

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    path_to_file, file_name = split(path)
    rename(path, path_to_file + '\\' + fernet.decrypt(file_name.encode()).decode())


async def decrypt_file(path: str, fernet: object):
    """
    This function is used to combine the 2 function above
    1) Call the decrypt file content function
    2) Call the decrypt file name function

    :param path: The path of the file
    :param fernet: Fernet object loaded with the key used to crypt
    """
    try:
        await asyncio.gather(decrypt_file_content(path, fernet), decrypt_file_name(path, fernet))
    except RuntimeError:
        print("Error during decrypt file :" + path)
