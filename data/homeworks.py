#  Nikulin Vasily © 2021
import sqlalchemy

from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = 'homeworks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    date = sqlalchemy.Column(sqlalchemy.String)
    lesson_number = sqlalchemy.Column(sqlalchemy.Integer)
    homework = sqlalchemy.Column(sqlalchemy.String)
