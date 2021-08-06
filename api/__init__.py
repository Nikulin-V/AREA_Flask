#  Nikulin Vasily © 2021
from flask import Blueprint
from tools.io_blueprint import IOBlueprint

api = Blueprint('api', __name__)
sock = IOBlueprint()

# noinspection PyPep8
from . import companies
from . import news
from . import offers
from . import sessions
from . import stocks
from . import svotes
from . import users
from . import votes
from . import wallets
