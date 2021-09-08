#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Stock(SqlAlchemyBase):
    __tablename__ = 'stocks'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    session = relationship('Session')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = relationship('User')
    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"))
    company = relationship('Company')
    stocks = sqlalchemy.Column(sqlalchemy.Integer)
