#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import json
import os
from os.path import exists

CONFIG_FILE_PATH = os.environ['USERPROFILE'] + "\\Documents\\" + \
                   os.getenv("CONFIG_FILE_NAME") + '.json'


def create_config_file(computer_id: int):
    """
    This function is used to get the computer id stored in a json config file
    1) Open the config file
    2) Return the computer_id of the json config file
    :param computer_id: The ID of the computer
    """

    payload = json.dumps({
        "computer_id": computer_id,
        "encrypted": True,
        "has_paid": False
    })

    if not exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w+", encoding="utf-8") as config_file:
            config_file.write(payload)


def edit_config_file(field: str, value: str):
    """
    This function is used to edit the data stored in a json config file
    1) Check if the file exist
    2) Open the config file
    3) Change a property value specify in parameter
    :param value: The new value for the field
    :param field: The field to change the value
    """
    if exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r+", encoding="utf-8") as config_file:
            json_data = json.load(config_file)
            json_data[field] = value
            config_file.seek(0)
            config_file.write(json.dumps(json_data))
            config_file.truncate()


def get_config_file_info(field: str):
    """
    This function is used to get an information stored in a json config file
    1) Check if the file exist
    2) Open the config file
    3) Return the value of the filed given in param
    :param field: The field that we want the value
    """

    if exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_file:
            json_file = json.load(config_file)
            return json_file[field]

    return -1
