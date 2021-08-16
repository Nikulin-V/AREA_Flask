#  Nikulin Vasily © 2021
from flask import request
from flask_login import login_required, current_user

from area.api import clients_sid, socket


@socket.on('registerUserSessionSID')
@login_required
def registerUserSessionSID():
    clients_sid[current_user.id] = request.sid
