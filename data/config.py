from .db_session import SqlAlchemyBase
import sqlalchemy


class Constant(SqlAlchemyBase):
    __tablename__ = 'config'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.VARCHAR)
