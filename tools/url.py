#  Nikulin Vasily © 2021
from flask import url_for

from config import SCHEME


def url(endpoint, **kwargs):
    return url_for(endpoint, _scheme=SCHEME, _external=True, **kwargs)
