#  Nikulin Vasily © 2021
from flask import Blueprint

market = Blueprint('market', __name__, subdomain='market')

from .companies import companies_voting
from .company_panel import company_panel
from .create_company import create_company
from .game_result import game_result
from .marketplace import marketplace
from .news import news
from .session_panel import session_panel
from .sessions import sessions
from .user_panel import user_panel
from .voting import stockholders_voting
