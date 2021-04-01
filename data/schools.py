from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class School(SqlAlchemyBase):
    __tablename__ = 'schools'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.String)
    director_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    head_teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
