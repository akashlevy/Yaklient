# -*- coding: utf-8 -*-

"""Treat yaklient as package"""

import settings
from yaklient import config
from yaklient.objects.location import Location
from yaklient.objects.user import NoBasecampSetError, TooCloseToSchoolException
from yaklient.objects.user import User

__title__ = 'yaklient'
__author__ = 'Akash Levy'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Akash Levy'