#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Constant(SqlAlchemyBase):
    __tablename__ = 'config'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    session = relationship('Session')
    name = sqlalchemy.Column(sqlalchemy.String)
    value = sqlalchemy.Column(sqlalchemy.VARCHAR)
