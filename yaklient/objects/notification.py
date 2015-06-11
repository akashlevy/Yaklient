# -*- coding: utf-8 -*-

"""Class for a notification on Yik Yak"""

from yaklient.api import notifyapi
from yaklient.helper import emoji_remove, ParsingResponseError


def check_notif_error(raw):
    """Make sure the raw response from manipulating notifications does not
    contain an error"""
    try:
        if raw.json()["error"] != {}:
            return False
        else:
            return True
    except (KeyError, ValueError):
        raise ParsingResponseError("Error marking notifications", raw)


class Notification(object):
    """A notification from Yik Yak"""
    def __init__(self, raw, user):
        """Initialize notification from raw JSON dict and user"""
        self.body = raw["body"]
        self.content = raw["content"]
        self.count = raw["count"]
        self.created_time = raw["created"]
        self.key = raw["key"]
        self.notif_id = raw["_id"]
        self.priority = raw["priority"]
        self.read = raw["subject"]
        self.reason = raw["reason"]
        self.status = raw["status"]
        self.subject = raw["subject"]
        self.thing_id = raw["thingID"]
        self.thing_type = raw["thingType"]
        self.updated_time = raw["updated"]
        self.user = user
        try:
            self.reply_id = raw["replyId"]
        except KeyError:
            self.reply_id = None
        try:
            self.hash_key = raw["hash_key"]
            self.__v = raw["__v"]
        except KeyError:
            self.hash_key = None
            self.__v = None

    def __str__(self):
        """Return notifications as string"""
        string = "Notification subject: %s (%s)\n%s"
        return string % (self.subject, self.status, emoji_remove(self.body))

    def _mark(self, status):
        """Mark the notification with status on the notify server. Return
        True if no error, False if error in response"""
        notif_id = self.notif_id
        user_id = self.user.user_id
        raw = notifyapi.update_batch([notif_id], status, user_id)
        return check_notif_error(raw)

    def mark_read(self):
        """Mark the notification as read locally and on the notify server.
        Return True if successful, False if unsuccessful"""
        if self._mark("read"):
            self.read = True
            return True
        return False

    def mark_unread(self):
        """Mark the notification as unread locally and on the notify server.
        Return True if successful, False if unsuccessful"""
        if self._mark("unread"):
            self.read = False
            return True
        return False

    def update(self):
        """Update properties from Yik Yak. Return True if successful, False
        if unsuccessful"""
        for notif in self.user.get_notifications():
            if notif.notif_id == self.notif_id:
                self = notif
                return True
        return False
