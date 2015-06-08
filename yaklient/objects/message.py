# -*- coding: utf-8 -*-

"""Abstract class for a post on Yik Yak"""

from abc import abstractmethod
from yaklient import helper


class Message(object):
    """An abstract class for a postable object on Yik Yak (Comment or Yak)"""
    def __init__(self, raw, user):
        """Initialize message from raw JSON dict and user"""
        self.delivery_id = raw["deliveryID"]
        self.liked = raw["liked"]
        self.likes = raw["numberOfLikes"]
        self.message_id = helper.backslash_remove(raw["messageID"])
        self.poster_id = raw["posterID"]
        self.time = raw["time"]
        self.user = user
        try:
            self.reyaked = raw["reyaked"]
        except KeyError:
            self.reyaked = None

    @abstractmethod
    def __str__(self):
        """Return message as string"""
        pass

    def delete(self):
        """Delete message from Yik Yak. Return True if successful, False if
        unsuccessful"""
        return self.user.delete(self)

    def downvote(self):
        """Downvote the message. Return True if successful, False if
        unsuccessful"""
        if self.user.downvote(self):
            self.likes -= 1
            return True
        else:
            return False

    def get_comments(self):
        """Get comments on the message"""
        return self.user.get_comments(self)

    def post_comment(self, comment):
        """Post a comment on the message. Return True if successful, False if
        unsuccessful"""
        return self.user.post_comment(comment, self.message_id)

    def report(self):
        """Report a message to Yik Yak"""
        self.user.report(self)

    @abstractmethod
    def update(self):
        """Update properties from Yik Yak"""
        pass

    def upvote(self):
        """Upvote the message. Return True if successful, False if
        unsuccessful"""
        if self.user.upvote(self):
            self.likes += 1
            return True
        else:
            return False
