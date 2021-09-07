#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Wallet(SqlAlchemyBase):
    __tablename__ = 'wallets'
    excluded_columns = []

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    money = sqlalchemy.Column(sqlalchemy.REAL)

    user = relationship('User', primaryjoin='Wallet.user_id == User.id')

    def __str__(self):
        return str(round(self.money))
