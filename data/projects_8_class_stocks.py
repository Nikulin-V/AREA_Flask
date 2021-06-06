from .db_session import SqlAlchemyBase
import sqlalchemy


class Stock(SqlAlchemyBase):
    __tablename__ = '8_class_projects_stocks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("8_class_projects.id"))
    stocks = sqlalchemy.Column(sqlalchemy.Integer)
