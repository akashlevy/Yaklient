# -*- coding: utf-8 -*-

"""A low-level API for Yik Yak, providing access to all the basic functions"""

from requests import Session
from time import time
from urllib import urlencode, unquote
from urlparse import urljoin
from yaklient import settings
from yaklient.config import get_token, get_user_agent
from yaklient.helper import generate_id, hash_msg


# Session for requests
SESSION = Session()
REQUEST = SESSION.request


def _send(method, url, endpoint, params, data=None):
    """Return response from server after making request with method to endpoint
    with params and, optionally, data"""
    url = urljoin(url, endpoint)
    version = settings.YIKYAK_VERSION + settings.YIKYAK_VERSION_LETTER
    params += [("version", version)]
    salt = str(int(time()))
    msg = urljoin("/api/", endpoint) + '?' + unquote(urlencode(params)) + salt
    hash_string = hash_msg(settings.YIKYAK_APIKEY, msg)
    params += [("salt", salt), ("hash", hash_string)]
    if method == "POST":
        data = sorted(data + params)
    user_agent = get_user_agent()
    headers = {"User-Agent": user_agent, "Accept-Encoding": "gzip"}
    return REQUEST(method, url, params=params, data=data, headers=headers)


def register_user(user):
    """Return raw response data from registering user"""
    params = [("accuracy", user.location.accuracy),
              ("deviceID", generate_id(dashes=False, upper=True)),
              ("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "registerUser", params)


def get_message(user, message_id):
    """Return raw response data for a message (ID: message_id) using user"""
    params = [("accuracy", user.location.accuracy),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getMessage", params)


def get_messages(user, location, basecamp=0):
    """Return raw response data for all messages in location/basecamp using
    user"""
    if basecamp and location is None:
        location = user.basecamp_location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getMessages", params)


def get_peek_messages(user, peek_id):
    """Return raw response data for messages at peek location (ID: peek_id)
    using user"""
    params = [("accuracy", user.location.accuracy),
              ("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("peekID", peek_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getPeekMessages", params)


def hot(user, location, basecamp=0):
    """Return raw response data for top messages in location/basecamp using
    user"""
    if basecamp:
        location = user.basecamp_location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "hot", params)


def yaks(user, location):
    """Return raw response data for messages at location using user"""
    params = [("accuracy", user.location.accuracy),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "yaks", params)


def get_my_recent_yaks(user):
    """Return raw response data for recent Yaks of user"""
    params = [("accuracy", user.location.accuracy),
              ("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getMyRecentYaks", params)


def get_my_recent_replies(user):
    """Return raw response data for recent replies of user"""
    params = [("accuracy", user.location.accuracy),
              ("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getMyRecentReplies", params)


def get_my_tops(user):
    """Return raw response data for top Yaks of user"""
    params = [("accuracy", user.location.accuracy),
              ("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getMyTops", params)


def get_area_tops(user):
    """Return raw response data for top Yaks in area"""
    params = [("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getAreaTops", params)


def get_comments(user, message_id, basecamp=0):
    """Return raw response data for all comments on a message (ID: message_id)
    using user (optionally at basecamp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "getComments", params)


def like_message(user, message_id, basecamp=0):
    """Return raw response data from upvoting a message (ID: message_id) using
    user (optionally at basecamp)"""
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "likeMessage", params)


def downvote_message(user, message_id, basecamp=0):
    """Return raw response data from downvoting a message (ID: message_id)
    using user (optionally at basecamp)"""
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "downvoteMessage", params)


def like_comment(user, comment_id, basecamp=0):
    """Return raw response data from upvoting a comment (ID: comment_id) using
    user (optionally at basecamp)"""
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("commentID", comment_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "likeComment", params)


def downvote_comment(user, comment_id, message_id, basecamp=0):
    """Return raw response data from downvoting a comment (ID: comment_id)
    belonging to message (ID: message_id) using user (optionally at
    basecamp)"""
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("commentID", comment_id),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "downvoteComment", params)


def report_message(user, message_id, reason, basecamp=0):
    """Return raw response data from reporting a message (ID: message_id) for a
    specified reason using user (optionally at basecamp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("messageID", message_id),
              ("reason", reason),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "reportMessage", params)


def report_comment(user, comment_id, message_id, reason, basecamp=0):
    """Return raw response data from reporting a comment (ID: comment_id)
    belonging to message (ID: message_id) for a specified reason using user
    (optionally at basecamp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("commentID", comment_id),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("messageID", message_id),
              ("reason", reason),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "reportComment", params)


def delete_message(user, message_id, basecamp=0):
    """Return raw response data from deleting a message (ID: message_id)
    using user (optionally at basecamp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "deleteMessage2", params)


def delete_comment(user, comment_id, message_id, basecamp=0):
    """Return raw response data from deleting a comment (ID: comment_id)
    belonging to a message (ID: message_id) with user (optionally at
    basecamp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("commentID", comment_id),
              ("lat", location.latitude),
              ("long", location.longitude),
              ("messageID", message_id),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.YIKYAK_ENDPOINT, "deleteComment", params)


def log_event(user, event_type):
    """Return raw response data from logging an app event of type event_type
    using user"""
    params = [("accuracy", user.location.accuracy),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    data = [("eventType", event_type),
            ("lat", user.location.latitude),
            ("long", user.location.longitude)]
    return _send("POST", settings.YIKYAK_ENDPOINT, "logEvent", params, data)


def send_message(user, message, handle=None, btp=0, basecamp=0):
    """Return raw response data from sending a message with an optional handle
    using user (optionally at basecamp and optionally with parameter
    bypassedThreatPopup as btp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("bc", int(basecamp)),
              ("token", get_token()),
              ("userID", user.user_id)]
    data = [("bypassedThreatPopup", int(btp)),
            ("lat", location.latitude),
            ("long", location.longitude),
            ("message", message)]
    if handle:
        data += [("hndl", handle)]
    return _send("POST", settings.YIKYAK_ENDPOINT, "sendMessage", params, data)


def post_comment(user, comment, message_id, btp=0, basecamp=0):
    """Return raw response data from posting a comment belonging to message
    (ID: message_id) using user (optionally at basecamp and optionally with
    parameter bypassedThreatPopup as btp)"""
    if basecamp:
        location = user.basecamp_location
    else:
        location = user.location
    params = [("accuracy", user.location.accuracy),
              ("bc", int(basecamp)),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    data = [("bypassedThreatPopup", int(btp)),
            ("comment", comment),
            ("lat", location.latitude),
            ("long", location.longitude),
            ("messageID", message_id)]
    return _send("POST", settings.YIKYAK_ENDPOINT, "postComment", params, data)


def submit_peek_message(user, message, peek_id, handle=None, btp=0):
    """Return raw response data from submitting a peek message with an optional
    handle at peek location with ID peek_id using user (optionally with
    parameter bypassedThreatPopup as btp)"""
    params = [("token", get_token()),
              ("userID", user.user_id)]
    data = [("bypassedThreatPopup", int(btp)),
            ("lat", user.location.latitude),
            ("long", user.location.longitude),
            ("message", message),
            ("peekID", peek_id)]
    if handle:
        data += [("hndl", handle)]
    return _send("POST", settings.YIKYAK_ENDPOINT, "submitPeekMessage",
                 params, data)


def contact_us(user, message, category, email):
    """Return raw response data from contacting Yik Yak with message in
    particular category using user with specified email"""
    params = [("token", get_token()),
              ("userID", user.user_id)]
    data = [("category", category),
            ("email", email),
            ("message", message)]
    return _send("POST", settings.YIKYAK_ENDPOINT, "contactUs", params, data)


def get_basecamps(user):
    """Return raw response data for all basecamps of user"""
    params = [("lat", user.location.latitude),
              ("long", user.location.longitude),
              ("token", get_token()),
              ("userID", user.user_id),
              ("userLat", user.location.latitude),
              ("userLong", user.location.longitude)]
    return _send("GET", settings.BASECAMP_ENDPOINT, "getBasecamps", params)


def save_basecamp(user, name, location):
    """Return raw response data from saving a basecamp"""
    params = [("token", get_token()),
              ("userID", user.user_id)]
    data = [("bcLat", location.latitude),
            ("bcLong", location.longitude),
            ("bcName", name),
            ("bcPeekId", 0)]
    return _send("POST", settings.BASECAMP_ENDPOINT, "saveBasecamp", params,
                 data)
