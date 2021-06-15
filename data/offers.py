from .db_session import SqlAlchemyBase
import sqlalchemy


class Offer(SqlAlchemyBase):
    __tablename__ = 'marketplace'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("marketplace.id"))
    stocks = sqlalchemy.Column(sqlalchemy.Integer)
    reserved_stocks = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    price = sqlalchemy.Column(sqlalchemy.Integer)
