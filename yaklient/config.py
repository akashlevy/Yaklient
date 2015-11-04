# -*- coding: utf-8 -*-

"""Settings for Yik Yak and Parse APIs"""

import re
import yaklient.settings as settings
from hashlib import md5
from random import choice, randint
from requests import Session
from string import ascii_uppercase, digits
from yaklient.helper import ParsingResponseError
from yaklient.objects.location import Location


# Session for requests
SESSION = Session()
GET = SESSION.get


def get_sites():
    """Return list of websites that are allowed"""
    response = GET(settings.ALLOWED_SITES_URL)
    try:
        return response.json()
    except ValueError:
        raise ParsingResponseError("Failed to get allowed websites", response)


def get_config():
    """Return list of websites that are allowed"""
    key_list = ["yikYakRepApplicationConfiguration", "endpoints",
                "threat_checks", "default_endpoint", "shareThreshold"]
    try:
        response = GET(settings.CONFIG_URL)
        # Make sure all necessary keys are in dict
        if all(key in response.json()["configuration"] for key in key_list):
            return response.json()["configuration"]
        else:
            raise ParsingResponseError("Config settings missing", response)
    except ValueError:
        raise ParsingResponseError("Failed to get config settings", response)


def get_user_agent(append_yikyak_version=True):
    """Return the user agent to use for Yik Yak API queries"""
    if settings.RANDOMIZE_USER_AGENT:
        randomize_user_agent()
    user_agent = "%s/%s (Linux; U; Android %s; %s Build/%s)"
    user_agent %= (settings.VM_TYPE, settings.VM_VERSION,
                   settings.ANDROID_VERSION, settings.DEVICE, settings.BUILD)
    if append_yikyak_version:
        user_agent += " " + settings.YIKYAK_VERSION
        user_agent += settings.YIKYAK_VERSION_LETTER
    return user_agent


def randomize_user_agent():
    """Generate random user agent for Yik Yak API queries"""
    settings.VM_VERSION = choice(settings.VM_VERSIONS)
    settings.ANDROID_VERSION = choice(settings.ANDROID_VERSIONS)
    settings.DEVICE = choice(settings.DEVICES)

    # Build is random alphanumeric sequence with randomly chosen length
    settings.BUILD = ""
    for _ in range(choice(settings.BUILD_STRING_LENGTHS)):
        settings.BUILD += choice(ascii_uppercase + digits)


def randomize_endpoint():
    """Select random Yik Yak server to make requests from"""
    # Choose random location and locationize
    locationize_endpoint(Location(randint(-90, 90), randint(-180, 180)))


def reset_endpoint():
    """Select default Yik Yak server to make requests from"""
    settings.YIKYAK_ENDPOINT = get_default_endpoint()


def locationize_endpoint(location):
    """Select Yik Yak server based on location of request"""
    for endpoint in get_endpoints():
        min_loc = Location(endpoint["min_latitude"], endpoint["min_longitude"])
        max_loc = Location(endpoint["max_latitude"], endpoint["max_longitude"])
        if min_loc.longitude <= location.longitude <= max_loc.longitude:
            if min_loc.latitude <= location.latitude <= max_loc.latitude:
                settings.YIKYAK_ENDPOINT = endpoint["url"]
                return
    settings.YIKYAK_ENDPOINT = get_default_endpoint()


def get_endpoints():
    """Return list of endpoints from Yik Yak server"""
    conf = get_config()
    return conf["endpoints"]


def get_share_threshold():
    """Return share threshold from Yik Yak server"""
    conf = get_config()
    return int(conf["shareThreshold"]["shareThreshold"])


def get_famous_threshold():
    """Return famous threshold from Yik Yak server"""
    conf = get_config()
    return int(conf["shareThreshold"]["famousThreshold"])


def get_threat_checks():
    """Return a list of threat checks from Yik Yak server"""
    conf = get_config()
    return conf["threat_checks"]


def check_threats(message):
    """Return list of threats found in message"""
    threats = []
    for threat_check in get_threat_checks():
        for expression in threat_check["expressions"]:
            if re.search(expression, message, re.I | re.U):
                del threat_check["expressions"]
                threats += [threat_check]
                break
    return threats


def get_default_endpoint():
    """Return default endpoint from Yik Yak server"""
    conf = get_config()
    return conf["default_endpoint"]


def get_yakarma_threshold():
    """Return the Yakarma threshold from Yik Yak server"""
    conf = get_config()
    return int(conf["yikYakRepApplicationConfiguration"]["yakarmaThreshold"])


def get_token():
    """Return the token for authenticating request to the Yik Yak server"""
    user_agent = get_user_agent(append_yikyak_version=False)
    return md5(user_agent).hexdigest()    
