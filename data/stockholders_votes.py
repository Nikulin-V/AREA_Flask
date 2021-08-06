#  Nikulin Vasily © 2021
from uuid import uuid4
from .db_session import SqlAlchemyBase
import sqlalchemy


class SVote(SqlAlchemyBase):
    __tablename__ = 'stockholders_votes'

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"))
    action = sqlalchemy.Column(sqlalchemy.String)
    voted_stockholders_ids = sqlalchemy.Column(sqlalchemy.String)
