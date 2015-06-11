# -*- coding: utf-8 -*-

"""Tests the Yaklient package"""

from yaklient import Location
from yaklient import User
import time


# Testing location
TESTING_GROUNDS = Location(45, 75)


def upvote_timeout():
    """Find the approximate time to wait to upvote a Yak after creating user"""
    # Initialize
    user = User(TESTING_GROUNDS)
    user.post_yak("Test yak")
    yak = user.get_yaks()[0]

    # Wait for upvote to be processed
    print "Started timer"
    start_time = time.time()
    while yak.likes == 0:
        user.upvote_yak(yak)
        yak = user.get_yaks()[0]
        print yak
    end_time = time.time()

    # Print elapsed time
    elapsed_time = end_time - start_time
    print "Elapsed time: %f" % elapsed_time


def cupvote_timeout():
    """Find the approximate time to wait to upvote a comment after creating
    user"""
    # Initialize
    user = User(TESTING_GROUNDS)
    user.post_yak("Test yak")
    yak = user.get_yaks()[0]
    while not yak.loaded:
        yak = user.get_yaks()[0]
    user.post_comment("Test comment", yak)
    comment = user.get_comments(yak)[0]

    # Wait for upvote to be processed
    print "Started timer"
    start_time = time.time()
    while comment.likes == 0:
        user.upvote_comment(yak)
        yak = user.get_yaks()[0]
        print yak
    end_time = time.time()

    # Print elapsed time
    elapsed_time = end_time - start_time
    print "Elapsed time: %f" % elapsed_time


def downvote_timeout():
    """Find the approximate time to wait to downvote a Yak after creating
    user"""
    # Initialize
    user = User(TESTING_GROUNDS)
    user.post_yak("Test yak")
    yak = user.get_yaks()[0]

    # Wait for upvote to be processed
    print "Started timer"
    start_time = time.time()
    while yak.likes == 0:
        user.downvote_yak(yak)
        yak = user.get_yaks()[0]
        print yak
    end_time = time.time()

    # Print elapsed time
    elapsed_time = end_time - start_time
    print "Elapsed time: %f" % elapsed_time
