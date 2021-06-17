from .db_session import SqlAlchemyBase
import sqlalchemy


class Constant(SqlAlchemyBase):
    __tablename__ = 'config'

    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    value = sqlalchemy.Column()
