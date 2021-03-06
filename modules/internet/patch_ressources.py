#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""System modules"""
import datetime
import json
import os

import requests

from modules.internet.common import get_headers_content_type_json

WEB_SERVER_URL_COMPUTER_DETAIL_GET: str = os.getenv("WEB_SERVER_URL_COMPUTER_DETAIL_GET")


def patch_last_message_date(computer_id: int, date: datetime):
    """
    This function is used to change the last message date send by this computer to the web server
    1) Prepare the payload with the date given in param
    2) Make a PATCH request to the web server with the payload to PATCH the last_message_date
    :param date: the date now to send to the web server
    :param computer_id: the computer id (stored in config file)
    """

    payload = json.dumps({
        "last_message_date": str(date),
    })

    headers = get_headers_content_type_json()

    response = requests.request("PATCH", WEB_SERVER_URL_COMPUTER_DETAIL_GET +
                                str(computer_id) + "/", headers=headers,
                                data=payload)

    json_response = response.json()
    print(json_response)

    return json_response
