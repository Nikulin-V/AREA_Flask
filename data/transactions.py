#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy

from .db_session import SqlAlchemyBase


class Transaction(SqlAlchemyBase):
    __tablename__ = 'transactions'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    offer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("marketplace.id"))
    stocks = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Integer)
