# -*- coding: utf-8 -*-

"""Class for a location on Yik Yak"""


class Location(object):
    """Location including latitude, longitude, and accuracy"""
    def __init__(self, latitude, longitude, accuracy=None):
        """Initialize latitude, longitude, and accuracy"""
        if accuracy is None:
            accuracy = 20.0
        self.accuracy = float(accuracy)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        """Return location as string"""
        return "Location(%s, %s)" % (self.latitude, self.longitude)
