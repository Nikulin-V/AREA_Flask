#  Nikulin Vasily © 2021
from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from data import db_session
from data.companies import Company
from data.config import Constant
from data.groups import Group
from data.homeworks import Homework
from data.news import News
from data.roles import Role, RolesUsers
from data.scheduled_job import ScheduledJob
from data.schools import School
from data.sessions import Session
from data.stocks import Stock
from data.users import User
from data.wallets import Wallet


class BaseModelView(ModelView):
    column_auto_select_related = True
    column_hide_backrefs = True
    column_display_all_relations = True

    def __init__(self, model, session, **kwargs):
        super(BaseModelView, self).__init__(model, session, **kwargs)

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """

        if not current_user.is_authenticated:
            return abort(401)

        if not current_user.has_role('admin'):
            return abort(403)


class UserView(BaseModelView):
    column_exclude_list = ['hashed_password', 'epos_login', 'epos_password']


class NewsView(BaseModelView):
    column_exclude_list = ['liked_ids']


def connect_models(admin):
    db_sess = db_session.create_session()

    admin_models = [(User, UserView), RolesUsers, Role, ScheduledJob]
    market_models = [Session, Constant, (News, NewsView), Company, Stock, Wallet]
    edu_models = [School, Group, Homework]

    categories = {
        'Admin': admin_models,
        'Market': market_models,
        'Education': edu_models
    }

    for category, models in categories.items():
        for model in models:
            if isinstance(model, tuple):
                model_view = model[1]
                model = model[0]
                admin.add_view(model_view(model, db_sess, category=category))
            else:
                admin.add_view(BaseModelView(model, db_sess, category=category))
