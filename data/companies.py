#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy

from .db_session import SqlAlchemyBase


class Company(SqlAlchemyBase):
    __tablename__ = 'companies'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    sector = sqlalchemy.Column(sqlalchemy.String)
    logo_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    authors_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
