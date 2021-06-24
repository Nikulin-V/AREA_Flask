#  Nikulin Vasily (c) 2021

from .area_diary import area_diary_page
from .company_panel import company_panel_page
from .epos_diary import epos_diary_page
from .game_panel import game_panel_page
from .game_result import game_result_page
from .index import index_page
from .login import login_page
from .marketplace import marketplace_page
from .my_companies import my_companies_page
from .my_news import my_news_page
from .news import news_page
from .privacy_policy import privacy_policy_page
from .profile import profile_page
from .register import register_page
from .sessions import sessions_page
from .user_panel import user_panel_page
from .voting import voting_page

pages_blueprints = [login_page, register_page, profile_page,
                    privacy_policy_page,
                    # index_page, area_diary_page, epos_diary_page,
                    marketplace_page, voting_page, game_result_page,
                    user_panel_page, game_panel_page, company_panel_page,
                    news_page, my_news_page, sessions_page,
                    my_companies_page]
