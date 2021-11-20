#  Nikulin Vasily © 2021
from flask_login import current_user

from data import db_session
from data.roles import Role
from data.users import User
from edu.api import api, socket
from tools.tools import send_response, fillJson, roles_allowed


@socket.on('getTeachers')
@api.route('/api/teachers', methods=['GET'])
def getTeachers():
    event_name = 'getTeachers'

    db_sess = db_session.create_session()

    school_id = current_user.school_id
    teachers = list(filter(lambda user: user.has_role('teacher') or user.has_role('head_teacher'),
                           db_sess.query(User).filter(
                               User.school_id == school_id
                           ).all()))

    roles = list(map(lambda x: x[0], db_sess.query(Role.name).all()))
    teachers_data = []
    for teacher in teachers:
        teacher_roles = []
        for role in roles:
            if teacher.has_role(role):
                teacher_roles.append(role)
        teacher_dict = teacher.to_dict(only=('id', 'surname', 'name', 'patronymic', 'date_of_birth',
                                             'email', 'school_id', 'about', 'game_session_id'))
        teacher_dict['roles'] = teacher_roles
        teachers_data.append(teacher_dict)

    return send_response(
        event_name,
        {
            'message': 'Success',
            'users': teachers_data
        }
    )


@socket.on('editTeacher')
@api.route('/api/teachers', methods=['PUT'])
@roles_allowed('head_teacher', 'director')
def editTeacher(json=None):
    event_name = 'editTeacher'

    db_sess = db_session.create_session()

    keys = ['surname', 'name', 'patronymic', 'roles']
    fillJson(json, keys)

    teacher = db_sess.query(User).filter(
        User.school_id == current_user.school_id,
        User.surname == json['surname'],
        User.name == json['name'],
    ).first()

    teacher.patronymic = json['patronymic']
    teacher.clear_roles(['student', 'teacher', 'head_teacher'])
    teacher.add_roles(json['roles'])

    db_sess.merge(teacher)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
        }
    )


@socket.on('deleteTeacher')
@api.route('/api/teachers', methods=['DELETE'])
@roles_allowed('head_teacher', 'director')
def deleteTeacher(json=None):
    event_name = 'deleteTeacher'

    db_sess = db_session.create_session()

    keys = ['surname', 'name', 'patronymic', 'roles']
    fillJson(json, keys)

    teacher = db_sess.query(User).filter(
        User.school_id == current_user.school_id,
        User.surname == json['surname'],
        User.name == json['name'],
    ).first()

    teacher.patronymic = json['patronymic']
    teacher.clear_roles(['student', 'teacher', 'head_teacher'])

    db_sess.merge(teacher)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
        }
    )
