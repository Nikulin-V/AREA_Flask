from .db_session import SqlAlchemyBase
import sqlalchemy


class Company(SqlAlchemyBase):
    __tablename__ = 'companies'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    section = sqlalchemy.Column(sqlalchemy.String)
    authors_ids = sqlalchemy.Column(sqlalchemy.String)
