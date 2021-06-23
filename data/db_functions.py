from flask_login import current_user
from sqlalchemy import or_

from data.groups import Group
from data.students import Student
from . import db_session
from .db_session import create_session
from .sessions import Session


def repair_dependencies_students_and_groups():
    db_sess = create_session()
    groups_lists = list(db_sess.query(Group.id, Group.students_ids))
    for group_id, students in groups_lists:
        for student_id in list(map(int, str(students).split(','))):
            if len(list(db_sess.query(Student).filter(Student.user_id == student_id,
                                                      Student.group_id == group_id))) == 0:
                db_sess.add(Student(user_id=student_id, group_id=group_id))
    db_sess.commit()


def get_game_roles():
    roles = []
    if current_user:
        db_sess = db_session.create_session()

        identifier = str(current_user.id)
        session_id = current_user.game_session_id
        session = db_sess.query(Session).filter(Session.id == session_id).first()

        if session:
            if identifier in str(session.admins_ids).split(';'):
                roles.append('Admin')
            if identifier in str(session.players_ids).split(';'):
                roles.append('Player')

    return roles


def get_game_sessions():
    db_sess = db_session.create_session()

    identifier = str(current_user.id)

    data = db_sess.query(Session).filter(or_(Session.admins_ids.contains(str(identifier)),
                                             Session.players_ids.contains(str(identifier)))).all()

    sessions = []
    for session_id in range(len(data)):
        if identifier in str(data[session_id].admins_ids) or \
                identifier in str(data[session_id].players):
            sessions.append(data[session_id])

    sessions.sort(key=lambda x: x.title)

    return sessions
