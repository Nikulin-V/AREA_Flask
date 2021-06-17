#  Nikulin Vasily (c) 2021
from .control_panel import control_panel_page
from .epos_diary import epos_diary_page
from .error import error_page
from .index import index_page
from .login import login_page
from .news import news_page
from .privacy_policy import privacy_policy_page
from .profile import profile_page
from .marketplace import marketplace_page
from .voting import voting_page
from .register import register_page
from .area_diary import area_diary_page

pages_blueprints = [login_page, register_page, profile_page, error_page,
                    index_page, privacy_policy_page,
                    area_diary_page, epos_diary_page,
                    marketplace_page, voting_page,
                    control_panel_page, news_page]
