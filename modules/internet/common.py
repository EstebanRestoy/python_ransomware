#  Copyright (c) 2022. Esteban Restoy e.restoy24@gmail.com

"""system modules"""
import base64
import os


def get_headers():
    """
    This function return the header needed to call api routes
    """
    return {
        'Authorization': 'Basic ' + base64.b64encode((os.getenv("API_ADMIN_USERNAME") + ":" +
                                                      os.getenv("API_ADMIN_PASSWORD"))
                                                     .encode()).decode(),
    }


def get_headers_content_type_json():
    """
    This function return the header with json content type needed to call api routes
    """
    return {
        'Authorization': 'Basic ' + base64.b64encode((os.getenv("API_ADMIN_USERNAME") + ":" +
                                                      os.getenv("API_ADMIN_PASSWORD"))
                                                     .encode()).decode(),
        'Content-Type': 'application/json'
    }
