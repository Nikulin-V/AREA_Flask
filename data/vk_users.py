import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class VkUser(SqlAlchemyBase, UserMixin):
    __tablename__ = 'vk_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)

    last_message_id = sqlalchemy.Column(sqlalchemy.Integer)

    AREA_email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    AREA_hashed_password = sqlalchemy.Column(sqlalchemy.String)

    epos_login = sqlalchemy.Column(sqlalchemy.String)
    epos_password = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, password):
        self.AREA_hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.AREA_hashed_password, password)
