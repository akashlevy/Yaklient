# -*- coding: utf-8 -*-

"""An API for performing image uploads with Amazon Web Services"""

from email.Utils import formatdate
from requests import Session
from requests.auth import AuthBase
from urllib import urlencode
from urlparse import urljoin
from yaklient import settings
from yaklient.helper import generate_id, hash_msg


# Session for requests
session = Session()
request = session.request


def _new_object(object_name):
    """Return raw response data from creating a new object (name:
    object_name)"""
    url = urljoin(settings.AWS_UPLOAD_ENDPOINT, "upload") + '?'
    url += urlencode({"s3_object_name": object_name})
    return request("GET", url)


def upload_image(image):
    """Upload image to the AWS server"""
    # Create the object on the AWS server
    object_name = generate_id()
    response = _new_object(object_name)
    # Strip the query from the returned URL
    url = response.text[:response.text.find('?')]
    # Send the request
    auth = AWSAuth(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY,
                   settings.AWS_BUCKET, object_name)
    files = {"file": image}
    return request("POST", url, files=files, auth=auth)


class AWSAuth(AuthBase):
    """Authentication for a request to the AWS server"""
    def __init__(self, access_key, secret_key, bucket, filename):
        """Initialize access_key, secret_key, and resource
        (/bucket/filename)"""
        self.access_key = access_key
        self.secret_key = secret_key
        self.resource = "/%s/%s" % (bucket, filename)

    def __call__(self, r):
        """Implement the AWS authentication for request r"""
        date_string = formatdate()
        content_type = r.headers["Content-Type"]
        msg = "PUT\n\n%s\n%s\n%s" % (content_type, date_string, self.resource)
        signature = hash_msg(self.secret_key, msg)
        r.headers["Date"] = date_string
        r.headers['Authorization'] = "AWS %s:%s" % (self.access_key, signature)
        return r
