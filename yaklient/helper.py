# -*- coding: utf-8 -*-

"""Helper functions for the Yik Yak and Parse APIs"""

import hmac
from base64 import b64encode
from hashlib import sha1
from re import sub
from uuid import uuid4


def backslash_remove(text):
    """Return text without backslashes"""
    return text.replace('\\', '')


def emoji_remove(text):
    """Return text without emojis"""
    return sub('[^\x00-\x7F]', '', text)


def generate_id(dashes=True, upper=False):
    """Return ID with or without dashes as either uppercase or lowercase"""
    uuid = uuid4() if dashes else uuid4().get_hex()
    return str(uuid).upper() if upper else str(uuid)


def hash_msg(key, msg):
    """Return SHA1 hash from key and msg"""
    return b64encode(hmac.new(key, msg, sha1).digest())


class ParsingResponseError(Exception):
    """An error parsing a request"""
    def __init__(self, error_string, response):
        """Initialize the error message"""
        self.msg = "%s\nResponse:\n%s" % (error_string, response.text)
        super(ParsingResponseError, self).__init__(self.msg)
        self.response = response

    def __str__(self):
        """Return the error message"""
        return self.msg
