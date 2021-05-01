from .db_session import SqlAlchemyBase
import sqlalchemy


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    students_ids = sqlalchemy.Column(sqlalchemy.String)
