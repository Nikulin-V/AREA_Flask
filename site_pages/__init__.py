#  Nikulin Vasily (c) 2021
from .epos_diary import epos_diary_page
from .error import error_page
from .index import index_page
from .login import login_page
from .privacy_policy import privacy_policy_page
from .profile import profile_page
from .projects_marketplace import projects_marketplace_page
from .projects_voting import projects_voting_page
from .register import register_page
from .area_diary import area_diary_page

pages_blueprints = [login_page, register_page, profile_page, error_page,
                    index_page, privacy_policy_page,
                    area_diary_page, epos_diary_page,
                    projects_marketplace_page, projects_voting_page]
