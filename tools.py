# -*- coding: utf-8 -*-

"""Tests the Yaklient package"""

from yaklient import Location
from yaklient import User
import yaklient
import threading


def cdownvoter_helper(i, user, comment_id, message_id):
    """Helps downvote a comment with a multitude of users"""
    user.downvote_comment(comment_id, message_id)
    print "User %d downvoted" % i


def cdownvoter(comment_id, message_id, votes):
    """Downvotes a comment with a multitude of users"""
    princeton = Location(42.3744, -71.1169)
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
    princeton = Location(42.3744, -71.1169)
    user = User(princeton)
    for i in range(1, votes+1):
        user = User(princeton)
        print "Created user %d" % i
        threading.Timer(80, upvoter_helper, [i, user, message_id]).start()

# Import client classes from Yaklient
from yaklient import *

# Specify location of University of Exeter on a map
princeton = Location(40.3571, -74.6702)

# Create user object at University of Exeter with given userid
user = User(princeton)

# Get yaks, iterate through them, and print them
for yak in user.get_yaks():
    print yak, yak.message_id
