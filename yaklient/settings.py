# -*- coding: utf-8 -*-

"""Settings for Yik Yak and Parse APIs"""

# Yik Yak API Parameters
YIKYAK_APIKEY = "EF64523D2BD1FA21F18F5BC654DFC41B"
YIKYAK_ENDPOINT = "https://us-central-api.yikyakapi.net/api/"
YIKYAK_VERSION = "2.7.3"
YIKYAK_VERSION_LETTER = "e"


# Parse API Parameters
PARSE_APPID = "wMkdjBI4ircsNcRn8mXnBkgH0dwOcrkexrdMY3vY"
PARSE_CLIENTKEY = "GbNFwvFgoUu1wYuwIexNImy8bnSlNhqssG7gd53Y"
PARSE_ENDPOINT = "https://api.parse.com/2/"
PARSE_VERSION = "1.7.1"
PARSE_VERSION_LETTER = "a"
PARSE_BUILD = "59"
PARSE_API_LEVEL = "22"


# Notify API Parameters
NOTIFY_ENDPOINT = "https://notify.yikyakapi.net/api/"


# Basecamp API Parameters
BASECAMP_ENDPOINT = "https://bc.yikyakapi.net/api/"


# Amazon S3 API Parameters (AWS_SECRET_KEY unknown)
AWS_ACCESS_KEY = "AKIAJFD2ANADKEMPW52A"
AWS_BUCKET = "photos-upload-yy"
AWS_SECRET_KEY = None
AWS_UPLOAD_ENDPOINT = "http://signedup.yikyakapi.net/upload"


# Yik Yak Settings Parameters
ALLOWED_SITES_URL = "http://lv.yikyakapi.net/getSites"
CONFIG_URL = "https://d3436qb9f9xu23.cloudfront.net/yikyak-config-android.json"


# Device Settings (for User Agent)
VM_TYPE = "Dalvik"
VM_VERSION = "2.1.0"
ANDROID_VERSION = "5.1"
DEVICE = "Android SDK built for x86"
BUILD = "LKY45"


# Options for randomize_user_agent()
VM_VERSIONS = ["2.1.0"]
ANDROID_VERSIONS = ["5.1"]
BUILD_STRING_LENGTHS = [5]
DEVICES = ["Nexus 4", "Nexus 5", "HTC One_M8", "SM-N900V", "XT1080",
           "SM-G900V", "SCH-I545", "Android SDK built for x86"]


# Randomization options
RANDOMIZE_USER_AGENT = False
RANDOMIZE_ENDPOINT = False
LOCATIONIZE_ENDPOINT = False


# Logging options
LOG_USERIDS = True


# Other Yik Yak-related parameters
NO_YAKS_MESSAGE_ID = "Y/b3c6c56b0305f2bc794e40b504f7150f"
TOO_CLOSE_TO_SCHOOL_MESSAGE_ID = "Y/1687dcbe8ca5a308d46c44343a4c69eb"
CONTACT_US_REASONS = ["My Basecamp location is wrong.",
                      "I'm not near a high school but it says I am! Help!",
                      "I want my college to be a Peek location!",
                      "I have a really cool idea for the app.",
                      "Yik Yak isn't working properly on my phone.",
                      "Someone posted something and I want it taken down.",
                      "My Yakarma has been reset.", "I forgot my pin code.",
                      "Other"]
