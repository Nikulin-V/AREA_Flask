#  Nikulin Vasily © 2021
from flask import Blueprint

edu = Blueprint('edu', __name__, subdomain='edu')

from .area_diary import area_diary
from .epos_diary import epos_diary
