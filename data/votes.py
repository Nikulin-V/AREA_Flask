#  Nikulin Vasily © 2021
from uuid import uuid4
from .db_session import SqlAlchemyBase
import sqlalchemy


class Vote(SqlAlchemyBase):
    __tablename__ = 'votes'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    company_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("companies.id"))
    points = sqlalchemy.Column(sqlalchemy.Integer)
