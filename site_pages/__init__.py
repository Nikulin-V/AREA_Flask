#  Nikulin Vasily (c) 2021
from .game_panel import game_panel_page
from .game_result import game_result_page
from .user_panel import user_panel_page
from .epos_diary import epos_diary_page
from .index import index_page
from .login import login_page
from .news import news_page
from .privacy_policy import privacy_policy_page
from .profile import profile_page
from .marketplace import marketplace_page
from .voting import voting_page
from .register import register_page
from .area_diary import area_diary_page

pages_blueprints = [login_page, register_page, profile_page,
                    index_page, privacy_policy_page,
                    area_diary_page, epos_diary_page,
                    marketplace_page, voting_page, game_result_page,
                    user_panel_page, game_panel_page, news_page]
