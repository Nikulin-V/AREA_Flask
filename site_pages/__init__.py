#  Nikulin Vasily © 2021

from .edu.area_diary import area_diary_page
from .edu.epos_diary import epos_diary_page

from .market.company_panel import company_panel_page
from .market.session_panel import game_panel_page
from .market.session_result import game_result_page
from .market.marketplace import marketplace_page
from .market.create_company import my_companies_page
from .market.news import news_page
from .market.sessions import sessions_page
from .market.user_panel import user_panel_page
from .market.companies import companies_page
from .market.voting import companies_management_page

from .index import index_page
from .login import login_page
from .register import register_page
from .profile import profile_page
from .privacy_policy import privacy_policy_page
from .yandex_verification import yandex_verification_page

pages_blueprints = [login_page, register_page, profile_page,
                    privacy_policy_page, index_page,
                    area_diary_page, epos_diary_page,
                    # company_panel_page,
                    marketplace_page, companies_page, companies_management_page, game_result_page,
                    user_panel_page, game_panel_page,
                    news_page, sessions_page,
                    my_companies_page, yandex_verification_page]
