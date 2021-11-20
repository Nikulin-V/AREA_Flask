#  Nikulin Vasily © 2021
from flask_login import current_user

from data import db_session
from data.classes import Class
from edu.api import api, socket
from tools.tools import send_response, fillJson, roles_allowed


@socket.on('getClasses')
@api.route('/api/classes', methods=['GET'])
def getClasses():
    event_name = 'getClasses'

    db_sess = db_session.create_session()

    classes = list(db_sess.query(Class).filter(
        Class.school_id == current_user.school_id
    ).all())

    classes.sort(key=lambda x: str(x.number) + str(x.letter))

    return send_response(
        event_name,
        {
            'message': 'Success',
            'classes': [
                {
                    'number': c.number,
                    'letter': c.letter
                }
                for c in classes
            ]
        }
    )


@socket.on('createClass')
@api.route('/api/classes', methods=['POST'])
@roles_allowed('head_teacher', 'director')
def createClass(json=None):
    if json is None:
        json = dict()

    event_name = 'createClass'
    fillJson(json, ['number', 'letter'])

    if not (json['number'] and json['letter']):
        return send_response(
            {
                'message': 'Error',
                'errors': ['Specify number and letter of class']
            }
        )

    db_sess = db_session.create_session()

    school_class = Class(
        number=int(json['number']),
        letter=json['letter'],
        school_id=current_user.school_id
    )

    # TODO: Обработать ошибку в JS
    if (school_class.number, school_class.letter) in db_sess.query(Class.number,
                                                                   Class.letter).all():
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Class already exists']
            }
        )

    db_sess.add(school_class)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success'
        }
    )


@socket.on('editClass')
@api.route('/api/classes', methods=['PUT'])
@roles_allowed('head_teacher', 'director')
def editClass(json=None):
    event_name = 'editClass'

    db_sess = db_session.create_session()

    keys = ['number', 'letter', 'old_number', 'old_letter']
    fillJson(json, keys)

    if not all([json[arg] for arg in keys]):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Not enough data']
            }
        )

    school_class = db_sess.query(Class).filter(
        Class.number == int(json['old_number']),
        Class.letter == json['old_letter'],
        Class.school_id == current_user.school_id
    ).first()

    school_class.letter = json['letter']
    school_class.number = json['number']

    db_sess.merge(school_class)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
        }
    )


@socket.on('deleteClass')
@api.route('/api/classes', methods=['DELETE'])
@roles_allowed('head_teacher', 'director')
def deleteClass(json=None):
    event_name = 'deleteClass'

    db_sess = db_session.create_session()

    keys = ['number', 'letter']
    fillJson(json, keys)

    school_class = db_sess.query(Class).filter(
        Class.number == int(json['number']),
        Class.letter == json['letter'],
        Class.school_id == current_user.school_id
    ).first()

    db_sess.delete(school_class)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
        }
    )
