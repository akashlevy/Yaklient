# -*- coding: utf-8 -*-

"""An API for retrieving Yik Yak notifications"""

import json
from requests import Session
from urlparse import urljoin
from yaklient import settings


# Session for requests
SESSION = Session()
REQUEST = SESSION.request


def get_all_for_user(user_id):
    """Return raw response data for all notifications of user (ID: user_id)"""
    url = urljoin(settings.NOTIFY_ENDPOINT, "getAllForUser/")
    url = urljoin(url, user_id)
    return REQUEST("GET", url)


def update_batch(notification_ids, status, user_id):
    """Return raw response data from updating the status of a batch
    of notifications for user (ID: user_id)"""
    data = {
            "notificationIDs": notification_ids,
            "status": status,
            "userID": user_id
            }
    url = urljoin(settings.NOTIFY_ENDPOINT, "updateBatch/")
    return REQUEST("POST", url, data=json.dumps(data))
