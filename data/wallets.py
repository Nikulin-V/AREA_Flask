from .db_session import SqlAlchemyBase
import sqlalchemy


class Wallet(SqlAlchemyBase):
    __tablename__ = 'wallets'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    session_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sessions.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"),
                                primary_key=True)
    money = sqlalchemy.Column(sqlalchemy.REAL, default=0)
