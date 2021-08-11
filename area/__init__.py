#  Nikulin Vasily © 2021
from flask import Blueprint

area = Blueprint('area', __name__, template_folder='templates')

from .index import index
from .error_page import error_page
from .login import login, logout
from .privacy_policy import privacy_policy
from .profile import profile
from .register import register
from .user_admin_panel import user_panel
from .verification import yandex_verification
