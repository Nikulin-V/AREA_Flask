from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    school_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("school_classes.id"))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    students_ids = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relation('User')
