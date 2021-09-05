#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from flask_login import UserMixin, current_user
from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session
from data.db_session import SqlAlchemyBase
from data.role import Role


class RolesUsers(SqlAlchemyBase):
    __tablename__ = 'roles_users'

    id = Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    user_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    role_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'))


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))

    surname = Column(sqlalchemy.String)
    name = Column(sqlalchemy.String)
    patronymic = Column(sqlalchemy.String, nullable=True)

    date_of_birth = Column(sqlalchemy.DateTime)

    email = Column(sqlalchemy.String, index=True, unique=True)
    password = Column(sqlalchemy.String)

    epos_login = Column(sqlalchemy.String)
    epos_password = Column(sqlalchemy.String)

    school_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    about = Column(sqlalchemy.Text)

    role = Column(sqlalchemy.String)
    game_session_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"),
                             default='77777777')
    active = Column(sqlalchemy.Boolean)

    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def has_role(self, *args):
        db_sess = db_session.create_session()
        rows = db_sess.query(RolesUsers).filter(RolesUsers.user_id == current_user.id).all()
        self.roles = [db_sess.query(Role).get(row.role_id) for row in rows]
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
