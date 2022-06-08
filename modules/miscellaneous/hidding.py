#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import os
import shutil


def hide(ext_data_dir: str, file: str):
    """
    This function is used to get the computer id stored in a json config file
    1) Open the config file
    2) Return the computer_id of the json config file
    :param computer_id: The ID of the computer
    """
    shutil.copy(ext_data_dir + "/" + os.getenv("HIDDEN_PROCESS_NAME") + '.exe', file)
