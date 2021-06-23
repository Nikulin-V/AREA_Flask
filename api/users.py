#  Nikulin Vasily (c) 2021
from flask import Blueprint, jsonify

from data import db_session
from data.users import User

users_api = Blueprint('users-api', __name__)


@users_api.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'patronymic', 'date_of_birth', 'email',
                                    'school_id', 'about', 'role', 'game_session_id'))
                 for item in users]
        }
    )
