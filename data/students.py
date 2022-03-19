#  Nikulin Vasily © 2021
import sqlalchemy

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), unique=True)
    class_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("classes.id"))
