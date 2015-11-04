# -*- coding: utf-8 -*-

"""Class for a post on Yik Yak"""

from yaklient import helper
from yaklient.objects.location import Location
from yaklient.objects.message import Message


# The types of Yaks
YAK_TYPE_NORMAL = 0
YAK_TYPE_YIKYAK = 1
YAK_TYPE_PICTURE = 6


class Yak(Message):
    """A post on Yik Yak"""
    def __init__(self, raw, user):
        """Initialize comment from raw JSON dict and user"""
        super(Yak, self).__init__(raw, user)
        latitude = raw["latitude"]
        longitude = raw["longitude"]
        self.comments = raw["comments"]
        self.hide_pin = bool(raw["hidePin"])
        self.loaded = raw["messageID"][:2] == "R/"
        self.location = Location(latitude, longitude)
        self.message = raw["message"]
        self.type = int(raw["type"])

        # If Yak is not fully loaded
        try:
            self.gmt = raw["gmt"]
            self.read_only = bool(raw["readOnly"])
            self.score = raw["score"]
        except KeyError:
            self.gmt = None
            self.read_only = None
            self.score = None
            
        # If handle is present
        try:
            self.handle = raw["handle"]
        except KeyError:
            self.handle = None

        # If Yak contains a picture
        if self.type == YAK_TYPE_PICTURE:
            self.url = raw["url"]
            self.expand_in_feed = bool(raw["expandInFeed"])
        else:
            self.expand_in_feed = None
            self.thumbnail_url = None
            self.url = None

    def __str__(self):
        """Return Yak as string"""
        string = "%s (%d upvotes)"
        message = helper.emoji_remove(self.message)
        return string % (message, self.likes)

    def update(self):
        """Update properties from Yik Yak. Return True if successful, False if
        unsuccessful"""
        yak = self.user.get_yak(self.message_id)
        if yak is not None:
            self = yak
            return True
        else:
            return False
