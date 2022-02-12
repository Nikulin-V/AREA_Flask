#  Nikulin Vasily © 2021
from flask_login import current_user

from data import db_session
from data.homeworks import Subject
from data.users import User
from edu.api import socket, api
from tools.tools import send_response


@socket.on('getSubjects')
@api.route('/api/subjects', methods=['GET'])
def getSubjects():
    event_name = 'getSubjects'

    db_sess = db_session.create_session()

    subjects = list(db_sess.query(Subject.title).all())

    return send_response(
        event_name,
        {
            'message': 'Success',
            'subjects': sorted(list(map(lambda x: x[0], subjects)))
        }
    )


@socket.on('getTeachersList')
@api.route('/api/teachers-info', methods=['GET'])
def getTeachersList():
    event_name = 'getTeachersList'

    db_sess = db_session.create_session()

    school_id = current_user.school_id
    teachers = list(filter(lambda user: user.has_role('teacher'),
                           db_sess.query(User).filter(
                               User.school_id == school_id
                           ).all()))

    teachers_data = [f'{t.surname} {t.name} {t.patronymic}' for t in teachers]

    return send_response(
        event_name,
        {
            'message': 'Success',
            'teachers': sorted(teachers_data)
        }
    )
