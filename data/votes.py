#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy

from .db_session import SqlAlchemyBase


class Vote(SqlAlchemyBase):
    __tablename__ = 'votes'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    company_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("companies.id"))
    sector = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("companies.sector"))
    points = sqlalchemy.Column(sqlalchemy.Integer)
