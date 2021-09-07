#  Nikulin Vasily © 2021
import werkzeug.routing
from flask import url_for

from config import SCHEME


def url(endpoint, **kwargs):
    try:
        return url_for(endpoint, _scheme=SCHEME, _external=True, **kwargs)
    except werkzeug.routing.BuildError:
        return url_for('area' + endpoint, _scheme=SCHEME, _external=True, **kwargs)
