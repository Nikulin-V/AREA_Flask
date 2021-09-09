#  Nikulin Vasily © 2021
from flask_login import current_user

from edu.api import api, socket
from data import db_session
from data.users import User
from tools.tools import send_response


@socket.on('getTeachers')
@api.route('/api/teachers', methods=['GET'])
def getTeachers():
    event_name = 'getTeachers'

    db_sess = db_session.create_session()

    school_id = current_user.school_id
    teachers = list(filter(lambda user: user.has_role('teacher'), db_sess.query(User).filter(
        User.school_id == school_id
    ).all()))

    return send_response(
        event_name,
        {
            'message': 'Success',
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'patronymic', 'date_of_birth', 'email',
                                    'school_id', 'about', 'game_user_id'))
                 for item in teachers]
        }
    )


# @socket.on('getTeachers')
# @api.route('/api/teachers', methods=['GET'])
# def getTeachers():
#     event_name = 'getTeachers'
#
#     db_sess = db_session.create_session()
#
#     school_id = current_user.school_id
#     teachers = list(filter(lambda user: user.has_role('teacher'), db_sess.query(User).filter(
#         User.school_id == school_id
#     ).all()))
#
#     return send_response(
#         event_name,
#         {
#             'message': 'Success',
#             'users':
#                 [item.to_dict(only=('id', 'surname', 'name', 'patronymic', 'date_of_birth', 'email',
#                                     'school_id', 'about', 'game_user_id'))
#                  for item in teachers]
#         }
#     )
