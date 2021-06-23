import sqlalchemy
from sqlalchemy_serializer import SerializerMixin


from .db_session import SqlAlchemyBase


class Session(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'sessions'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)

    title = sqlalchemy.Column(sqlalchemy.String)
    admins_ids = sqlalchemy.Column(sqlalchemy.String)
    players_ids = sqlalchemy.Column(sqlalchemy.String)
