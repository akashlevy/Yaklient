# -*- coding: utf-8 -*-

"""Class for a user on Yik Yak"""

from yaklient import helper
from yaklient import settings
from yaklient.api import notifyapi, parseapi, yikyakapi
from yaklient.objects.comment import Comment
from yaklient.objects.location import Location
from yaklient.objects.message import Message
from yaklient.objects.notification import Notification, check_notif_error
from yaklient.objects.peeklocation import PeekLocation
from yaklient.objects.yak import Yak
from yaklient.config import locationize_endpoint
from yaklient.helper import ParsingResponseError


class User(object):
    """A user who interacts with Yik Yak"""
    def __init__(self, location, user_id=None):
        """Initialize user with location and user_id"""
        self.basecamp_location = None
        self.basecamp_name = None
        self.basecamp_set = False
        self.location = location
        self.user_id = user_id
        self.yakarma = None
        # Set endpoint to nearest server if required
        if settings.LOCATIONIZE_ENDPOINT:
            locationize_endpoint(self.location)
        # If no user ID specified, register new user
        if self.user_id is None:
            self.user_id = helper.generate_id(dashes=False, upper=True)
            # Do not register with Parse if APPID or CLIENTKEY is missing
            if None in [settings.PARSE_APPID, settings.PARSE_CLIENTKEY]:
                self.register(parse_register=False)
            else:
                self.register()
            # Log user ID in file if required
            if settings.LOG_USERIDS:
                with open("userids", "a") as userid_file:
                    userid_file.write(self.user_id + "\n")
        # Update user properties from server
        self.update()

    def __str__(self):
        """Return user (user ID) as string"""
        return "User(%s) at %s" % (self.user_id, str(self.location))

    def _convert_to_comment_id(self, comment, yak):
        """Return comment_id and message_id from comment and yak"""
        # Get message_id from yak
        if yak is not None:
            message_id = self._convert_to_message_id(yak)
        # If comment is a Comment, use comment's comment_id and message_id
        if isinstance(comment, Comment):
            comment_id = comment.comment_id
            message_id = comment.message_id
        # If comment is a string, treat comment as the comment_id
        elif isinstance(comment, basestring):
            comment_id = comment
        # Otherwise, TypeError
        else:
            raise TypeError("comment is not Message/string: " + str(comment))
        try:
            return comment_id, message_id
        except NameError:
            raise NameError("No Yak specified")

    @staticmethod
    def _convert_to_message_id(yak):
        """Return message_id from yak"""
        # If yak is a Message, use yak's message_id
        if isinstance(yak, Message):
            message_id = yak.message_id
        # If yak is a string, treat yak as the message_id
        elif isinstance(yak, basestring):
            message_id = yak
        # Otherwise, TypeError
        else:
            raise TypeError("yak is not Message/string: " + str(yak))
        return message_id

    @staticmethod
    def _convert_to_peek_id(peek):
        """Return peek_id from peek"""
        # If peek is a PeekLocation, use peek's peek_id
        if isinstance(peek, PeekLocation):
            peek_id = peek.peek_id
        # If peek is a string, treat peek as the peek_id
        elif isinstance(peek, basestring):
            peek_id = peek
        # Otherwise, TypeError
        else:
            raise TypeError("peek is not Message/string" + str(peek))
        return peek_id

    def _get_comment_list(self, raw_data):
        """Return list of comments from raw"""
        try:
            return [Comment(raw, self) for raw in raw_data.json()["comments"]]
        except (KeyError, ValueError):
            raise ParsingResponseError("Getting comment list failed", raw_data)

    def _get_notification_list(self, raw_data):
        """Return list of Yaks from raw server response"""
        try:
            return [Notification(raw, self) for raw in raw_data.json()["data"]]
        except (KeyError, ValueError):
            raise ParsingResponseError("Getting notifs failed", raw_data)

    def _get_peek_location_list(self, raw_data, categ):
        """Return list of peek locations in category (categ) from raw"""
        try:
            return [PeekLocation(raw, self) for raw in raw_data.json()[categ]]
        except (KeyError, ValueError):
            raise ParsingResponseError("Getting peek list failed", raw_data)

    def _get_yak_list(self, raw_data):
        """Return list of Yaks from raw"""
        try:
            yaks = [Yak(raw, self) for raw in raw_data.json()["messages"]]
        except (KeyError, ValueError):
            raise ParsingResponseError("Getting Yak list failed", raw_data)
        # If no Yaks, return empty list
        if yaks == []:
            return yaks
        # If no user-created Yaks in given area, return empty list
        if yaks[0].message_id == settings.NO_YAKS_MESSAGE_ID:
            return []
        # If too close to school, raise exception
        elif yaks[0].message_id == settings.TOO_CLOSE_TO_SCHOOL_MESSAGE_ID:
            raise TooCloseToSchoolException("School nearby/invalid location")
        return yaks

    def _validate_basecamp(self, basecamp):
        """Raise error if basecamp is True but user has not set basecamp"""
        if basecamp and not self.basecamp_set:
            raise NoBasecampSetError("Tried to use basecamp when not set")

    def register(self, parse_register=True, yikyak_register=True):
        """Register with Parse (if parse_register is True) and Yik Yak (if
        yikyak_register is True). Return True if successful, False if
        unsuccessful"""
        if parse_register:
            parseapi.register_user(self.user_id)
        if yikyak_register:
            return bool(int(yikyakapi.register_user(self).text))

    def update(self):
        """Update Yakarma and basecamp information"""
        raw = yikyakapi.get_messages(self, self.location, basecamp=True)
        # Check if too close to school
        self._get_yak_list(raw)
        try:
            self.yakarma = int(raw.json()["yakarma"])
        except (KeyError, ValueError):
            raise ParsingResponseError("Getting Yakarma failed", raw)
        try:
            self.basecamp_set = bool(int(raw.json()["bcEligible"]))
        except (KeyError, ValueError):
            raise ParsingResponseError("Getting bcEligible failed", raw)
        try:
            latitude = float(raw.json()["bcLat"])
            longitude = float(raw.json()["bcLong"])
            self.basecamp_name = raw.json()["bcName"]
            self.basecamp_location = Location(latitude, longitude)
        except (KeyError, ValueError):
            pass

    def get_yak(self, yak):
        """Return Yak (or None if it does not exist)"""
        message_id = self._convert_to_message_id(yak)
        raw = yikyakapi.get_message(self, message_id)
        try:
            return self._get_yak_list(raw)[0]
        except IndexError:
            return None

    def get_yaks(self, location=None, basecamp=False):
        """Return a list of Yaks at particular location (optionally at
        basecamp)"""
        # Set location if not None, otherwise set to user's location
        location = location if location else self.location
        self._validate_basecamp(basecamp)
        raw = yikyakapi.get_messages(self, location, basecamp)
        return self._get_yak_list(raw)

    def get_featured_peek_locations(self):
        """Return a list of featured peek locations"""
        raw = yikyakapi.get_messages(self, self.location)
        return self._get_peek_location_list(raw, "featuredLocations")

    def get_other_peek_locations(self):
        """Return a list of other peek locations"""
        raw = yikyakapi.get_messages(self, self.location)
        return self._get_peek_location_list(raw, "otherLocations")

    def get_peek_yaks(self, location):
        """Return a list of Yaks at particular location/peek location"""
        # If location is a PeekLocation, use get_peek_messages
        if isinstance(location, PeekLocation):
            raw = yikyakapi.get_peek_messages(self, location.peek_id)
        # If location is a Location, use yaks
        elif isinstance(location, Location):
            raw = yikyakapi.yaks(self, location)
        # Otherwise, TypeError
        else:
            raise TypeError("location is not Location or PeekLocation")
        return self._get_yak_list(raw)

    def get_top_yaks(self, location=None, basecamp=False):
        """Return a list of the top Yaks at location/basecamp"""
        # Set location if not None, otherwise set to user's location
        location = location if location else self.location
        self._validate_basecamp(basecamp)
        raw = yikyakapi.hot(self, location, basecamp)
        return self._get_yak_list(raw)

    def get_user_recent_yaks(self):
        """Return a list of recent Yaks by user"""
        raw = yikyakapi.get_my_recent_yaks(self)
        return self._get_yak_list(raw)

    def get_user_recent_commented(self):
        """Return a list of Yaks with comments by user"""
        raw = yikyakapi.get_my_recent_replies(self)
        return self._get_yak_list(raw)

    def get_user_top_yaks(self):
        """Return a list of top Yaks by user"""
        raw = yikyakapi.get_my_tops(self)
        return self._get_yak_list(raw)

    def get_area_top_yaks(self):
        """Return a list of top Yaks in the area"""
        raw = yikyakapi.get_area_tops(self)
        return self._get_yak_list(raw)

    def get_comment(self, comment, yak=None, basecamp=False):
        """Return comment on a Yak (or None if it does not exist, optionally
        at basecamp)"""
        self._validate_basecamp(basecamp)
        (comment_id, message_id) = self._convert_to_comment_id(comment, yak)
        for comment in self.get_comments(message_id, basecamp=basecamp):
            if comment_id == comment.comment_id:
                return comment
        return None

    def get_comments(self, yak, basecamp=False):
        """Return a list of comments on a Yak (optionally at basecamp)"""
        self._validate_basecamp(basecamp)
        message_id = self._convert_to_message_id(yak)
        raw = yikyakapi.get_comments(self, message_id, basecamp)
        return self._get_comment_list(raw)

    def upvote(self, message, basecamp=False):
        """Upvote/unupvote a message (Yak/comment, optionally at basecamp).
        Return True if successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        if isinstance(message, Yak):
            return self.upvote_yak(message, basecamp=basecamp)
        elif isinstance(message, Comment):
            return self.upvote_comment(message, basecamp=basecamp)
        else:
            raise TypeError("yak is not Message")

    def downvote(self, message, basecamp=False):
        """Downvote/undownvote a message (Yak/comment, optionally at basecamp).
        Return True if successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        if isinstance(message, Yak):
            return self.downvote_yak(message, basecamp=basecamp)
        elif isinstance(message, Comment):
            return self.downvote_comment(message, basecamp=basecamp)
        else:
            raise TypeError("yak is not Message")

    def upvote_yak(self, yak, basecamp=False):
        """Upvote/unupvote a Yak (optionally at basecamp). Return True if
        successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        message_id = self._convert_to_message_id(yak)
        liked = self.get_yak(message_id).liked
        yikyakapi.like_message(self, message_id, basecamp)
        self.update()
        return self.get_yak(message_id).text != liked

    def downvote_yak(self, yak, basecamp=False):
        """Downvote/undownvote a Yak (optionally at basecamp). Return True if
        successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        message_id = self._convert_to_message_id(yak)
        liked = self.get_yak(message_id).liked
        yikyakapi.downvote_message(self, message_id, basecamp)
        self.update()
        return self.get_yak(message_id).liked != liked

    def upvote_comment(self, comment, yak=None, basecamp=False):
        """Upvote/unupvote a comment (optionally at basecamp). Return True if
        successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        (comment_id, message_id) = self._convert_to_comment_id(comment, yak)
        liked = self.get_comment(message_id, comment_id).liked
        yikyakapi.like_comment(self, comment_id, basecamp)
        self.update()
        return self.get_comment(message_id, comment_id).liked != liked

    def downvote_comment(self, comment, yak=None, basecamp=False):
        """Downvote/undownvote a comment (optionally at basecamp). Return True
        if successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        (comment_id, message_id) = self._convert_to_comment_id(comment, yak)
        liked = self.get_comment(message_id, comment_id).liked
        yikyakapi.downvote_comment(self, comment_id, basecamp)
        self.update()
        return self.get_comment(message_id, comment_id).liked != liked

    def report(self, message, reason, basecamp=False):
        """Report a message (Yak/comment) for reason (optionally at
        basecamp)"""
        self._validate_basecamp(basecamp)
        if isinstance(message, Yak):
            self.report_yak(message, reason, basecamp=basecamp)
        elif isinstance(message, Comment):
            self.report_comment(message, reason, basecamp=basecamp)
        else:
            raise TypeError("yak is not Message")

    def report_yak(self, yak, reason, basecamp=False):
        """Report a Yak for reason (optionally at basecamp)"""
        self._validate_basecamp(basecamp)
        message_id = self._convert_to_message_id(yak)
        yikyakapi.report_message(self, message_id, reason, basecamp)

    def report_comment(self, comment, reason, yak=None, basecamp=False):
        """Report a comment for reason (optionally at basecamp)"""
        self._validate_basecamp(basecamp)
        (comment_id, message_id) = self._convert_to_comment_id(comment, yak)
        yikyakapi.report_comment(self, comment_id, message_id, reason,
                                 basecamp)

    def delete(self, message, basecamp=False):
        """Delete a message (Yak/comment, optionally at basecamp). Return True
        if successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        if isinstance(message, Yak):
            return self.delete_yak(message, basecamp=basecamp)
        elif isinstance(message, Comment):
            return self.delete_comment(message, basecamp=basecamp)
        else:
            raise TypeError("yak is not Message")

    def delete_yak(self, yak, basecamp=False):
        """Delete a Yak (optionally at basecamp). Return True if successful,
        False if unsuccessful"""
        self._validate_basecamp(basecamp)
        message_id = self._convert_to_message_id(yak)
        yikyakapi.delete_message(self, message_id, basecamp)
        return self.get_yak(message_id) is None

    def delete_comment(self, comment, yak=None, basecamp=False):
        """Delete a comment (optionally at basecamp). Return True if
        successful, False if unsuccessful"""
        self._validate_basecamp(basecamp)
        (comment_id, message_id) = self._convert_to_comment_id(comment, yak)
        print comment_id, message_id
        yikyakapi.delete_comment(self, comment_id, message_id, basecamp)
        return self.get_comment(comment_id, message_id) is None

    def post_yak(self, message, handle=None, btp=False, basecamp=False):
        """Post a Yak with optional handle (optionally at basecamp and
        optionally with parameter bypassedThreatPopup as btp). Return the Yak
        once loaded (or None if not posted)"""
        self._validate_basecamp(basecamp)
        raw = yikyakapi.send_message(self, message, handle, btp, basecamp)
        # Yaks only post if get_messages is called directly after
        yikyakapi.get_messages(self, self.location, basecamp=basecamp)
        self.update()
        # If success is reported
        if bool(int(raw.text)):
            try:
                return self.get_yaks(basecamp=basecamp)[0]
            except IndexError:
                return None
        else:
            return None

    def post_comment(self, comment, yak, btp=False, basecamp=False):
        """Post a comment on a yak (optionally at basecamp and optionally with
        parameter bypassedThreatPopup as btp). Return the comment (or None if
        not posted)"""
        self._validate_basecamp(basecamp)
        message_id = self._convert_to_message_id(yak)
        raw = yikyakapi.post_comment(self, comment, message_id, btp, basecamp)
        # Comments only post properly if get_comments is called directly after
        yikyakapi.get_comments(self, message_id, basecamp=basecamp)
        self.update()
        # If success is reported
        if bool(int(raw.text)):
            try:
                return self.get_comments(message_id, basecamp=basecamp)[-1]
            except IndexError:
                return None
        else:
            return None

    def submit_peek_yak(self, message, peek, handle=None, btp=False):
        """Submit a message with optional handle for review to a peek location
        (ID: peek_id)"""
        peek_id = self._convert_to_peek_id(peek)
        yikyakapi.submit_peek_message(self, message, peek_id, handle, btp)

    def contact_yikyak(self, message, category, email):
        """Send Yik Yak a message in particular category with specified
        email"""
        yikyakapi.contact_us(self, message, category, email)

    def get_notifications(self):
        """Get all notifications for user"""
        raw = notifyapi.get_all_for_user(self.user_id)
        return self._get_notification_list(raw)

    def _mark_notifications(self, status):
        """Mark all notifications for user as read"""
        notif_ids = [notif.notif_id for notif in self.get_notifications()]
        raw = notifyapi.update_batch(notif_ids, status, self.user_id)
        check_notif_error(raw)

    def mark_notifications_read(self):
        """Mark all notifications for user as read"""
        return self._mark_notifications("read")

    def mark_notifications_unread(self):
        """Mark all notifications for user as unread"""
        return self._mark_notifications("unread")

    def set_basecamp(self, name, location=None):
        """Set the basecamp to location with name. Return True if successful,
        False if unsuccessful"""
        # Set location if not None, otherwise set to user's location
        location = location if location else self.location
        raw = yikyakapi.save_basecamp(self, name, location)
        self.update()
        try:
            return raw.json()["saveBasecamp"]
        except (KeyError, ValueError):
            raise ParsingResponseError("Setting basecamp failed", raw)


class NoBasecampSetError(Exception):
    """Exception that is raised when trying to access non-existent basecamp"""
    pass


class TooCloseToSchoolException(Exception):
    """Exception that is raised when location is too close to a school"""
    pass
