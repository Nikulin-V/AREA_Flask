#  Nikulin Vasily © 2021
from uuid import uuid4
from .db_session import SqlAlchemyBase
import sqlalchemy


class Constant(SqlAlchemyBase):
    __tablename__ = 'config'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    name = sqlalchemy.Column(sqlalchemy.String)
    value = sqlalchemy.Column(sqlalchemy.VARCHAR)
