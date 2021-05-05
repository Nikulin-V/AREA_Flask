from .db_session import SqlAlchemyBase
import sqlalchemy


class Homework(SqlAlchemyBase):
    __tablename__ = 'homeworks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    date = sqlalchemy.Column(sqlalchemy.Date)
    homework = sqlalchemy.Column(sqlalchemy.String)
