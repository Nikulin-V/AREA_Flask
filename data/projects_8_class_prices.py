from .db_session import SqlAlchemyBase
import sqlalchemy


class Price(SqlAlchemyBase):
    __tablename__ = '8_class_projects_prices'

    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("8_class_projects.id"), primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
