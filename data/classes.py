#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    number = Column(sqlalchemy.Integer, nullable=True)
    letter = Column(sqlalchemy.String, nullable=True)
    school_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    school = relationship('School')
    teacher_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    teacher = relationship('User')

    def __str__(self):
        return f'{self.number}{self.letter}'


class ClassLesson(SqlAlchemyBase):
    __tablename__ = 'class_lessons'

    id = Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    class_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("classes.id"))
    school_class = relationship('Class')
    lesson = Column(sqlalchemy.String)


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    school_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("schools.id"))
    school = relationship('School')
    title = Column(sqlalchemy.String, nullable=True)
    subject = Column(sqlalchemy.String)
    class_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("classes.id"))
    school_class = relationship('Class')
    teacher_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    teacher = relationship('User')
    students_ids = Column(sqlalchemy.String)
    schedule = Column(sqlalchemy.String)


class GroupLesson(SqlAlchemyBase):
    __tablename__ = 'group_lessons'

    id = Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    group_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("groups.id"))
    group = relationship('Group')
    class_lesson_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("class_lessons.id"))
    hours = Column(sqlalchemy.Integer, default=0)
    teacher_id = Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    teacher = relationship('User')
