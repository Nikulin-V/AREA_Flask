from .db_session import SqlAlchemyBase
import sqlalchemy


class Stock(SqlAlchemyBase):
    __tablename__ = 'stocks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"))
    stocks = sqlalchemy.Column(sqlalchemy.Integer)
