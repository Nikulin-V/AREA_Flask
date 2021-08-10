#  Nikulin Vasily © 2021
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from uuid import uuid4
from .db_session import SqlAlchemyBase


class Session(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'sessions'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    admins_ids = sqlalchemy.Column(sqlalchemy.String)
    players_ids = sqlalchemy.Column(sqlalchemy.String)
