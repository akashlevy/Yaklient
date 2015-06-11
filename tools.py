# -*- coding: utf-8 -*-

"""Tests the Yaklient package"""

from yaklient import Location
from yaklient import User
import threading


def cdownvoter_helper(i, user, comment_id, message_id):
    """Helps downvote a comment with a multitude of users"""
    user.downvote_comment(comment_id, message_id)
    print "User %d downvoted" % i


def cdownvoter(comment_id, message_id, votes):
    """Downvotes a comment with a multitude of users"""
    princeton = Location(40.3487, -74.6593)
    user = User(princeton)
    for i in range(1, votes+1):
        user = User(princeton)
        print "Created user %d" % i
        args = [i, user, comment_id, message_id]
        threading.Timer(10, cdownvoter_helper, args).start()


def upvoter_helper(i, user, message_id):
    """Helps upvote a Yak with a multitude of users"""
    user.upvote_yak(message_id)
    print "User %d upvoted" % i


def upvoter(message_id, votes):
    """Helps upvote a Yak with a multitude of users"""
    princeton = Location(40.3487, -74.6593)
    user = User(princeton)
    for i in range(1, votes+1):
        user = User(princeton)
        print "Created user %d" % i
        threading.Timer(80, upvoter_helper, [i, user, message_id]).start()
