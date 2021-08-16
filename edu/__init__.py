#  Nikulin Vasily © 2021
from flask import Blueprint

edu = Blueprint('edu', __name__, subdomain='edu', template_folder='templates')

from .index import index
from .area_diary import area_diary
from .epos_diary import epos_diary
from .errors import error_page
