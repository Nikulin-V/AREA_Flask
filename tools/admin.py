#  Nikulin Vasily © 2021
from flask import abort, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from data import db_session
from data.companies import Company
from data.config import Constant
from data.groups import Group
from data.homeworks import Homework
from data.news import News
from data.offers import Offer
from data.role import Role
from data.scheduled_job import ScheduledJob
from data.schools import School
from data.sessions import Session
from data.stockholders_votes import SVote
from data.stocks import Stock
from data.students import Student
from data.users import User
from data.vk_users import VkUser
from data.votes import Vote
from data.wallets import Wallet


class MyModelView(ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                return abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


def connect_models(admin):
    db_sess = db_session.create_session()
    models = [User, Role, Company, Constant, Group, Homework, News, Offer, ScheduledJob, School,
              Session, SVote, Stock, Student, VkUser, Vote, Wallet]
    for model in models:
        admin.add_view(MyModelView(model, db_sess))
