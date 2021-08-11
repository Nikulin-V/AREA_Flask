#  Nikulin Vasily © 2021
import datetime
from uuid import uuid4

import sqlalchemy

from data.db_session import SqlAlchemyBase


class ScheduledJob(SqlAlchemyBase):
    __tablename__ = 'scheduled_job'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    model = sqlalchemy.Column(sqlalchemy.String)
    object_id = sqlalchemy.Column(sqlalchemy.String)
    action = sqlalchemy.Column(sqlalchemy.String)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now() + datetime.timedelta(1))
