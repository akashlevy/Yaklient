# -*- coding: utf-8 -*-

"""Class for a peek location on Yik Yak"""

from yaklient.objects.location import Location


class PeekLocation(Location):
    """A peek location: a remote location for viewing Yaks"""
    def __init__(self, raw, user):
        """Initialize peek location from raw JSON dict"""
        latitude = float(raw["latitude"])
        longitude = float(raw["longitude"])
        accuracy = float(raw["delta"])*1E4
        super(PeekLocation, self).__init__(latitude, longitude, accuracy)
        self.can_reply = bool(raw["canReply"])
        self.can_report = bool(raw["canReport"])
        self.can_submit = bool(raw["canSubmit"])
        self.can_vote = bool(raw["canVote"])
        self.is_local = bool(raw["isLocal"])
        self.inactive = bool(raw["inactive"])
        self.location = raw["location"]
        self.peek_id = raw["peekID"]
        self.photos_enabled = bool(raw["photosEnabled"])
        self.user = user
        try:
            self.is_fictional = bool(raw["isFictional"])
        except KeyError:
            self.is_fictional = None

    def __str__(self):
        """Return peek location as string"""
        return self.location + ": Peek" + super(PeekLocation, self).__str__()

    def get_yaks(self):
        """Return Yaks at this peek location"""
        return self.user.get_peek_yaks(self.peek_id)

    def submit_yak(self, message, handle=None):
        """Submit a Yak with message and optionally handle to this peek
        location"""
        return self.user.submit_peek_yak(message, self.peek_id, handle)
