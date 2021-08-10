#  Nikulin Vasily © 2021
from flask import Blueprint

area = Blueprint('area', __name__)

from .index import index
from .login import login, logout
from .privacy_policy import privacy_policy
from .profile import profile
from .register import register
from .user_admin_panel import user_panel
from .yandex_verification import yandex_verification
