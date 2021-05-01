from .db_session import SqlAlchemyBase
import sqlalchemy


class Student(SqlAlchemyBase):
    __tablename__ = 'student'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), unique=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    marks = sqlalchemy.Column(sqlalchemy.String, nullable=True)
