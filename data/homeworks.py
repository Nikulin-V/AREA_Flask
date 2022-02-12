#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy

from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = 'homeworks'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    date = sqlalchemy.Column(sqlalchemy.String)
    lesson_number = sqlalchemy.Column(sqlalchemy.Integer)
    homework = sqlalchemy.Column(sqlalchemy.String)


class Subject(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String)


class Workload(SqlAlchemyBase):
    __tablename__ = 'workload'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    school_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("schools.id"))
    title = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("subjects.title"))
    teacher_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"),
                                   nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("classes.id"))
    group_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hours = sqlalchemy.Column(sqlalchemy.Integer, default=0)
