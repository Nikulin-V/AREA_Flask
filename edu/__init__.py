#  Nikulin Vasily © 2021
from flask import Blueprint

from .api import api, socket

edu = Blueprint('edu', __name__, subdomain='edu', template_folder='templates',
                static_folder='static', static_url_path='/edu/static')
edu.register_blueprint(api)

from .index import index
from .area_diary import area_diary
from .epos_diary import epos_diary
from .errors import error_page
from .staff import staff
