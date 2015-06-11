# -*- coding: utf-8 -*-

"""An API for Yik Yak's Parse service"""

import json
from requests import Session
from requests_oauthlib import OAuth1
from time import tzname
from urlparse import urljoin
from yaklient.helper import generate_id, ParsingResponseError
from yaklient import settings


# Session for requests
SESSION = Session()
REQUEST = SESSION.request


def _create_installation(iid):
    """Send a request to create an installation (ID: iid). Return the object
    ID associated with it"""
    data = {
            "deviceType": "android",
            "appVersion": settings.YIKYAK_VERSION,
            "parseVersion": settings.PARSE_VERSION,
            "appName": "Yik Yak",
            "timeZone": tzname[0],
            "installationId": iid,
            "appIdentifier": "com.yik.yak"
            }
    return _send("create", data, iid)


def _save_user(user_id, iid, object_id):
    """Send a request to add user_id to the installation with (ID: iid,
    object_id"""
    # User ID is surrounded by a 'c' on either side
    user_id = 'c' + user_id + 'c'
    data = {
            "channels": {"objects": [user_id], "__op": "AddUnique"},
            "objectId": object_id
            }
    return _send("update", data, iid)


def _send(method, data, iid):
    """Send data associated with an installation (ID: iid) to Yik Yak's Parse
    service using specified method. Return the response"""
    url = urljoin(settings.PARSE_ENDPOINT, method)
    data = {
            "classname": "_Installation",
            "data": data,
            "osVersion": settings.ANDROID_VERSION,
            "appBuildVersion": settings.PARSE_BUILD,
            "appDisplayVersion": settings.YIKYAK_VERSION,
            "v": settings.PARSE_VERSION_LETTER + settings.PARSE_VERSION,
            "iid": iid,
            "uuid": generate_id()
            }
    json_data = json.dumps(data)
    auth = OAuth1(settings.PARSE_APPID, settings.PARSE_CLIENTKEY)
    user_agent = "Parse Android SDK %s (com.yik.yak/%s) API Level %s"
    user_agent %= (settings.PARSE_VERSION, settings.PARSE_BUILD,
                   settings.PARSE_API_LEVEL)
    headers = {"Accept-Encoding": "gzip", "User-Agent": user_agent}
    return REQUEST("POST", url, data=json_data, auth=auth, headers=headers)


def register_user(user_id):
    """Register a user with Yik Yak's Parse service. Create a new installation
    and add user_id to it. Return installation ID and object ID"""
    # Installation ID
    iid = generate_id()
    # Create installation and check for errors
    response = _create_installation(iid)
    try:
        object_id = response.json()["result"]["data"]["objectId"]
    except (KeyError, ValueError):
        raise ParsingResponseError("Error creating installation", response)
    # Save user and check for errors and consistency
    response = _save_user(user_id, iid, object_id)
    try:
        if response.json()["result"]["data"]["channels"][0][1:-1] != user_id:
            raise ParsingResponseError("Error saving user", response)
    except (KeyError, ValueError):
        raise ParsingResponseError("Error saving user", response)
    return iid, object_id
