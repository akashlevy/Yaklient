# -*- coding: utf-8 -*-

"""Tests the Yaklient package"""

import unittest
import yaklient
from yaklient.helper import ParsingResponseError
from yaklient.objects.peeklocation import PeekLocation
from yaklient.objects.user import NoBasecampSetError, TooCloseToSchoolException
from yaklient.objects.yak import Yak


# Constants (test places and user IDs)
# A clean location has no Yaks
# A big location has a lot of Yaks
# The USER_IDS should also be "clean" i.e. no posts, no basecamp etc.
LOC_ZERO = yaklient.Location(0, 0)
CLEAR_LOC_1 = yaklient.Location(37.5, -47)
CLEAR_LOC_2 = yaklient.Location(37.5, -45)
BIG_LOC = yaklient.Location(40.3487, -74.6593)
USER_IDS = ["B24F242E876E4EBEA6133838BE3D22BC",
            "177E75DC97C0449788931D7BAAC42035",
            "ADE2EEA1D25949B698CC7DA0DB5C0049",
            "F07C535792074BD1BD05FAA881485F4A",
            "8B8D6407A281416A9B1AF880F0C7C21E"]


class TestYaklientObjects(unittest.TestCase):
    """Tests all methods in User"""
    def test_too_close_to_school_exception(self):
        """Location(0, 0) should produce a TooCloseToSchoolException"""
        self.assertRaises(TooCloseToSchoolException, yaklient.User, LOC_ZERO)

    def test_no_yaks(self):
        """Make sure a location with no Yaks returns an empty list"""
        user = yaklient.User(CLEAR_LOC_1)
        self.assertEqual(user.get_yaks(), [])

    def test_new_user_init(self):
        """Make sure a new user is initialized correctly"""
        user = yaklient.User(CLEAR_LOC_1)
        self.assertEqual(user.location, CLEAR_LOC_1)
        self.assertIs(user.basecamp_location, None)
        self.assertIs(user.basecamp_name, None)
        self.assertEqual(user.basecamp_set, False)
        self.assertEqual(user.yakarma, 100)

    def test_old_user_init(self):
        """Make sure an existing user is initialized correctly"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        self.assertEqual(user.location, CLEAR_LOC_1)
        self.assertIs(user.basecamp_location, None)
        self.assertEqual(user.user_id, USER_IDS[0])

    def test_update_failure(self):
        """Make sure update fails on bad user ID"""
        self.assertRaises(ParsingResponseError, yaklient.User, CLEAR_LOC_1, "")

    def test_get_featured_peek_locations(self):
        """Make sure get featured peek locations works. Also tests get peek
        Yaks"""
        user = yaklient.User(CLEAR_LOC_1)
        peek_locations = user.get_featured_peek_locations()
        self.assertNotEqual(peek_locations, [])
        self.assertIsInstance(peek_locations[0], PeekLocation)
        peek_yaks = user.get_peek_yaks(peek_locations[0])
        self.assertNotEqual(peek_yaks, [])
        self.assertIsInstance(peek_yaks[0], Yak)

    def test_get_other_peek_locations(self):
        """Make sure get other peek locations works. Also tests get peek
        Yaks"""
        user = yaklient.User(CLEAR_LOC_1)
        peek_locations = user.get_other_peek_locations()
        self.assertNotEqual(peek_locations, [])
        self.assertIsInstance(peek_locations[0], PeekLocation)
        peek_yaks = user.get_peek_yaks(peek_locations[0])
        self.assertNotEqual(peek_yaks, [])
        self.assertIsInstance(peek_yaks[0], Yak)

    def test_invalid_basecamp(self):
        """Make sure error is caught when basecamp is not set and it is
        used in a get_yaks request"""
        user = yaklient.User(CLEAR_LOC_1)
        self.assertRaises(NoBasecampSetError, user.get_yaks, basecamp=True)

    def test_set_basecamp(self):
        """Make sure updating basecamp updates user"""
        user = yaklient.User(CLEAR_LOC_1)
        basecamp_success = user.set_basecamp("Test Basecamp", CLEAR_LOC_2)
        self.assertEqual(basecamp_success, True)
        self.assertEqual(user.basecamp_name, "Test Basecamp")
        self.assertEqual(user.basecamp_set, True)

    def test_yak(self):
        """Make sure posting/retrieving/updating/deleting a Yak works"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        yak = user.post_yak("Test Message", "Hello")
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        yak.update()
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    def test_yak_basecamp(self):
        """Make sure posting/retrieving/updating/deleting a Yak works at
        basecamp"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        user.set_basecamp("Test Basecamp", CLEAR_LOC_2)
        yak = user.post_yak("Test Message", "Hello", basecamp=True)
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        yak.update()
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    def test_get_yaks(self):
        """Make sure getting Yaks at large place is successful"""
        user = yaklient.User(BIG_LOC)
        yaks = user.get_yaks()
        self.assertNotEqual(yaks, [])
        self.assertIsInstance(yaks[0], Yak)

    def test_get_top_yaks(self):
        """Make sure getting top Yaks at large place is successful"""
        user = yaklient.User(BIG_LOC)
        yaks = user.get_yaks()
        self.assertNotEqual(yaks, [])
        self.assertIsInstance(yaks[0], Yak)

    def test_get_user_top_yaks(self):
        """Make sure getting top Yaks for a user works"""
        user = yaklient.User(CLEAR_LOC_1)
        user.post_yak("Test Message", "Hello")
        yak = user.get_user_top_yaks()[0]
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        print yak.message_id
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    def test_get_area_top_yaks(self):
        """Make sure getting area top Yaks at large place is successful"""
        user = yaklient.User(BIG_LOC)
        yaks = user.get_area_top_yaks()
        self.assertNotEqual(yaks, [])
        self.assertIsInstance(yaks[0], Yak)

    def test_get_user_recent_yaks(self):
        """Make sure getting recent Yaks for a user works"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        user.post_yak("Test Message", "Hello")
        yak = user.get_user_recent_yaks()[0]
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    def test_get_user_recent_commented(self):
        """Make sure getting recently commented Yaks for a user works"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        yak = user.post_yak("Test Message", "Hello")
        user.post_comment("Test Comment", yak)
        yak = user.get_user_recent_commented()[0]
        self.assertEqual(yak.message, "Test Message")
        self.assertEqual(yak.handle, "Hello")
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    @unittest.skip("Haven't figured out commenting yet completely")
    def test_comment(self):
        """Make sure posting/retrieving/updating/deleting a comment works"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        yak = user.post_yak("Test Message", "Hello")
        comment = user.post_comment("Test Comment", yak)
        self.assertEqual(comment.comment, "Test Comment")
        comment.update()
        self.assertEqual(comment.comment, "Test Comment")
        delete_success = user.delete(comment)
        self.assertEqual(delete_success, True)
        self.assertEqual(comment.update(), False)
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    @unittest.skip("Haven't figured out commenting yet completely")
    def test_upvote(self):
        """Make sure upvoting Yaks/comments works"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        yak = user.post_yak("Test Message", "Hello")
        comment = user.post_comment("Test Comment", yak)
        upvote_comment_success = user.upvote(comment)
        upvote_yak_success = user.upvote(yak)
        self.assertEqual(upvote_comment_success, True)
        self.assertEqual(upvote_yak_success, True)
        self.assertEqual(yak.liked, True)
        self.assertEqual(yak.likes, 1)
        self.assertEqual(comment.liked, True)
        self.assertEqual(comment.likes, 1)
        upvote_comment_success = user.upvote(comment)
        upvote_yak_success = user.upvote(yak)
        self.assertEqual(upvote_comment_success, True)
        self.assertEqual(upvote_yak_success, True)
        self.assertEqual(yak.liked, True)
        self.assertEqual(yak.likes, 1)
        self.assertEqual(comment.liked, True)
        self.assertEqual(comment.likes, 1)
        delete_success = user.delete(comment)
        self.assertEqual(delete_success, True)
        self.assertEqual(comment.update(), False)
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    @unittest.skip("Haven't figured out commenting yet completely")
    def test_downvote(self):
        """Make sure downvoting Yaks/comments works"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        yak = user.post_yak("Test Message", "Hello")
        comment = user.post_comment("Test Comment", yak)
        upvote_comment_success = user.downvote(comment)
        upvote_yak_success = user.downvote(yak)
        self.assertEqual(upvote_comment_success, True)
        self.assertEqual(upvote_yak_success, True)
        self.assertEqual(yak.liked, True)
        self.assertEqual(yak.likes, 1)
        self.assertEqual(comment.liked, True)
        self.assertEqual(comment.likes, 1)
        upvote_comment_success = user.downvote(comment)
        upvote_yak_success = user.downvote(yak)
        self.assertEqual(upvote_comment_success, True)
        self.assertEqual(upvote_yak_success, True)
        self.assertEqual(yak.liked, True)
        self.assertEqual(yak.likes, 1)
        self.assertEqual(comment.liked, True)
        self.assertEqual(comment.likes, 1)
        delete_success = user.delete(comment)
        self.assertEqual(delete_success, True)
        self.assertEqual(comment.update(), False)
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    def test_report(self):
        """Make sure reporting Yaks/comments doesn't throw any exceptions"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        yak = user.post_yak("Test Message", "Hello")
        comment = user.post_comment("Test Comment", yak)
        user.report(yak, "Report")
        user.report(comment, "Report")
        delete_success = user.delete(yak)
        self.assertEqual(delete_success, True)
        self.assertEqual(yak.update(), False)

    def test_submit_peek_yak(self):
        """Make sure submitting a peek yak doesn't throw any exceptions"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        peek_locations = user.get_featured_peek_locations()
        user.submit_peek_yak("Test Message", peek_locations[0].peek_id, "Test")

    def test_contact_yikyak(self):
        """Make sure contacting Yik Yak doesn't throw any exceptions"""
        user = yaklient.User(CLEAR_LOC_1, USER_IDS[0])
        user.contact_yikyak("message", "category", "email")

    def test_empty_notifications(self):
        """Make sure a new user has no notifications"""
        user = yaklient.User(CLEAR_LOC_1)
        self.assertEqual(user.get_notifications(), [])

    @unittest.skip("Haven't figured out commenting yet completely")
    def test_notifications(self):
        """Make sure notifications can be created, read, and unread"""
        users = [yaklient.User(CLEAR_LOC_1, user_id) for user_id in USER_IDS]
        yak = users[0].post_yak("Test Message", "Hello")
        comment = users[0].post_comment("Test Comment", yak)
        for user in users:
            comment_downvote_success = user.downvote(comment)
            self.assertEqual(comment_downvote_success, True)
            yak_downvote_success = user.downvote(yak)
            self.assertEqual(yak_downvote_success, True)
        notifs = users[0].get_notifications()
        self.assertEqual(len(notifs), 2)
        self.assertEqual(notifs[0].status, "unread")
        self.assertEqual(notifs[1].status, "unread")
        mark_read_success = notifs[0].mark_read()
        self.assertEqual(mark_read_success, True)
        self.assertEqual(notifs[0].status, "read")
        mark_read_success = notifs[1].mark_read()
        self.assertEqual(mark_read_success, True)
        self.assertEqual(notifs[1].status, "read")
        mark_unread_success = notifs[0].mark_unread()
        self.assertEqual(mark_unread_success, True)
        self.assertEqual(notifs[0].status, "unread")
        mark_unread_success = notifs[1].mark_unread()
        self.assertEqual(mark_unread_success, True)
        self.assertEqual(notifs[1].status, "unread")
        users[0].mark_notifications_read()
        notifs = users[0].get_notifications()
        self.assertEqual(len(notifs), 2)
        self.assertEqual(notifs[0].status, "read")
        self.assertEqual(notifs[1].status, "read")
        users[0].mark_notifications_unread()
        notifs = users[0].get_notifications()
        self.assertEqual(len(notifs), 2)
        self.assertEqual(notifs[0].status, "unread")
        self.assertEqual(notifs[1].status, "unread")

def main():
    """Run the tests"""
    if __name__ == "__main__":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestYaklientObjects)
        unittest.TextTestRunner(verbosity=2).run(suite)

main()
