#  Nikulin Vasily © 2021
from flask import Blueprint
from flask_cors import CORS

from tools.io_blueprint import IOBlueprint

api = Blueprint('api', __name__)
CORS(api)
socket = IOBlueprint()

clients_sid = dict()

from .sockets import registerUserSessionSID
from .users import createUser, getUsers, editUser, deleteUser
