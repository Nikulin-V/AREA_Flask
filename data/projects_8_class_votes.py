from .db_session import SqlAlchemyBase
import sqlalchemy


class Vote(SqlAlchemyBase):
    __tablename__ = '8_class_projects_votes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("8_class_projects.id"))
    points = sqlalchemy.Column(sqlalchemy.Integer)
