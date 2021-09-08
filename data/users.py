#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db_session
from .db_session import SqlAlchemyBase
from .roles import RolesUsers, Role


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))

    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime)

    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    epos_login = sqlalchemy.Column(sqlalchemy.String)
    epos_password = sqlalchemy.Column(sqlalchemy.String)

    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('schools.id'))
    about = sqlalchemy.Column(sqlalchemy.Text)

    game_session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"),
                                        default='77777777')

    def has_role(self, role_name):
        db_sess = db_session.create_session()
        for role_id in db_sess.query(RolesUsers.role_id).filter(
                RolesUsers.user_id == self.id).all():
            if db_sess.query(Role).get(role_id).name == role_name:
                return True
        return False

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __str__(self):
        return f'{self.surname} {self.name} | {self.email}'
