from .db_session import SqlAlchemyBase
import sqlalchemy


class SVote(SqlAlchemyBase):
    __tablename__ = 'stockholders_votes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"))
    action = sqlalchemy.Column(sqlalchemy.String)
    voted_stockholders_ids = sqlalchemy.Column(sqlalchemy.String)
