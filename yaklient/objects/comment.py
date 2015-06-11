# -*- coding: utf-8 -*-

"""Class for a comment on Yik Yak"""

from yaklient import helper
from yaklient.objects.message import Message


class Comment(Message):
    """A comment on a post on Yik Yak"""
    def __init__(self, raw, user):
        """Initialize comment from raw JSON dict and user"""
        super(Comment, self).__init__(raw, user)
        self.comment = raw["comment"]
        self.comment_id = raw["commentID"]
        try:
            self.gmt = raw["gmt"]
        except KeyError:
            self.gmt = None
        try:
            self.back_id = raw["backID"]
            self.overlay_id = raw["overlayID"]
        except KeyError:
            self.back_id = None
            self.overlay_id = None
        try:
            self.text_style = raw["textStyle"]
        except KeyError:
            self.text_style = None

    def __str__(self):
        """Return comment as string"""
        return "%s (%d)" % (helper.emoji_remove(self.comment), self.likes)

    def update(self):
        """Update properties from Yik Yak. Return True if successful, False if
        unsuccessful"""
        comment = self.user.get_comment(self.comment_id, self.message_id)
        if comment is not None:
            self = comment
            return True
        else:
            return False
