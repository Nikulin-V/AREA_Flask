#  Nikulin Vasily © 2021
from flask_login import current_user

from data import db_session
from data.classes import Class
from data.homeworks import Workload
from data.users import User
from edu.api import api, socket
from tools.tools import send_response, fillJson, roles_allowed


@socket.on('getWorkload')
@api.route('/api/workload', methods=['GET'])
def getWorkload(json=None):
    if json is None:
        json = dict()

    event_name = 'getWorkload'
    fillJson(json, ['classNumber', 'classLetter'])

    if not (json['classNumber'] and json['classLetter']):
        return send_response(
            {
                'message': 'Error',
                'errors': ['Specify number and letter of class']
            }
        )

    db_sess = db_session.create_session()

    class_id = db_sess.query(Class.id).filter(
        Class.school_id == current_user.school_id,
        Class.number == json['classNumber'],
        Class.letter == json['classLetter']
    ).first()[0]

    workload = list(
        db_sess.query(
            Workload.title, Workload.hours, Workload.group_number, Workload.teacher_id
        ).filter(
            Workload.class_id == class_id
        ).all()
    )

    workload.sort(key=lambda x: x.title)

    hours = 0
    man_hours = 0
    lessons = set()
    for w in workload:
        man_hours += w[1]
        if (w[0], w[1]) not in lessons:
            lessons.add((w[0], w[1]))
            hours += w[1]

    return send_response(
        event_name,
        {
            'message': 'Success',
            'workload': [
                {
                    'title': w[0],
                    'hours': w[1],
                    'groupNumber': w[2],
                    'teacher': None if w[3] is None else
                    ' '.join([db_sess.query(User).get(w[3]).surname,
                              db_sess.query(User).get(w[3]).name,
                              db_sess.query(User).get(w[3]).patronymic]),
                }
                for w in workload
            ],
            'hours': hours,
            'manHours': man_hours
        }
    )


@socket.on('createWorkload')
@api.route('/api/workload', methods=['POST'])
@roles_allowed('head_teacher', 'director')
def createWorkload(json=None):
    if json is None:
        json = dict()

    event_name = 'createWorkload'
    fillJson(json, ['classNumber', 'classLetter', 'teacher', 'title', 'hours', 'groupNumber'])

    if not (json['classNumber'] and json['classLetter'] and json['title']
            and json['hours']):
        return send_response(
            {
                'message': 'Error',
                'errors': ['Not enough data']
            }
        )

    db_sess = db_session.create_session()

    workload = Workload(
        school_id=current_user.school_id,
        title=json['title'],
        teacher_id=get_teacher_id(json['teacher']),
        class_id=db_sess.query(Class.id).filter(
            Class.number == json['classNumber'],
            Class.letter == json['classLetter']
        ),
        group_number=json['groupNumber'],
        hours=json['hours']
    )

    db_sess.add(workload)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success'
        }
    )


@socket.on('editWorkload')
@api.route('/api/workload', methods=['PUT'])
@roles_allowed('head_teacher', 'director')
def editWorkload(json=None):
    if json is None:
        json = dict()

    event_name = 'editWorkload'
    fillJson(json,
             ['classNumber', 'classLetter',
              'oldTeacher', 'oldTitle', 'oldHours', 'oldGroupNumber',
              'teacher', 'title', 'hours', 'groupNumber'])

    if not (json['classNumber'] and json['classLetter'] and json['title']
            and json['hours'] is not None):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Not enough data']
            }
        )

    db_sess = db_session.create_session()

    workload = db_sess.query(Workload).filter(
        Workload.school_id == current_user.school_id,
        Workload.title == json['oldTitle'],
        Workload.teacher_id == get_teacher_id(json['oldTeacher']),
        Workload.class_id == db_sess.query(Class.id).filter(
            Class.number == json['classNumber'],
            Class.letter == json['classLetter']
        ),
        Workload.group_number == json['oldGroupNumber'],
        Workload.hours == json['oldHours']
    ).first()

    workload.teacher_id = get_teacher_id(json['teacher'])
    workload.title = json['title']
    workload.hours = json['hours']
    workload.group_number = json['groupNumber']

    db_sess.merge(workload)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success'
        }
    )


@socket.on('deleteWorkload')
@api.route('/api/workload', methods=['DELETE'])
@roles_allowed('head_teacher', 'director')
def deleteWorkload(json=None):
    if json is None:
        json = dict()

    event_name = 'deleteWorkload'
    fillJson(json, ['classNumber', 'classLetter', 'teacher', 'title', 'hours', 'groupNumber'])

    if not (json['classNumber'] and json['classLetter'] and json['title']
            and json['hours'] is not None):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Not enough data']
            }
        )

    db_sess = db_session.create_session()

    workload = db_sess.query(Workload).filter(
        Workload.school_id == current_user.school_id,
        Workload.title == json['title'],
        Workload.teacher_id == get_teacher_id(json['teacher']),
        Workload.class_id == db_sess.query(Class.id).filter(
            Class.number == json['classNumber'],
            Class.letter == json['classLetter']
        ).first()[0],
        Workload.group_number == json['groupNumber'],
        Workload.hours == json['hours']
    ).first()

    db_sess.delete(workload)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success'
        }
    )


def get_teacher_id(teacher):
    if teacher in ['null', 'Не назначен'] or teacher is None:
        return None
    db_sess = db_session.create_session()
    try:
        return db_sess.query(User.id).filter(
            User.surname == teacher.split()[0],
            User.name == teacher.split()[1],
            User.patronymic == teacher.split()[2]
        ).first()[0]
    except IndexError:
        return None
