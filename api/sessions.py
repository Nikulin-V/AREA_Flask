#  Nikulin Vasily (c) 2021
from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_

from data import db_session
from data.sessions import Session

sessions_api = Blueprint('sessions-api', __name__)


@sessions_api.route('/api/sessions')
def get_sessions():
    db_sess = db_session.create_session()
    sessions = db_sess.query(Session).all()
    return jsonify(
        {
            'sessions':
                [item.to_dict(only=('id', 'title', 'admins_ids', 'players_ids'))
                 for item in sessions]
        }
    )


@sessions_api.route('/api/create_session?title=<string:title>', methods=['POST'])
@login_required
def create_session(title):
    db_sess = db_session.create_session()
    session = Session(
        title=title,
        admins_ids=str(current_user.id)
    )
    db_sess.add(session)
    db_sess.commit()


@sessions_api.route('/api/edit_session_roles?'
                    'action=<string:action>&'
                    'role=<string:role>&'
                    'user_id=<int:user_id>',
                    methods=['POST'])
@login_required
def edit_session_roles(action, role, user_id):
    db_sess = db_session.create_session()
    session_id = current_user.game_session_id
    session = db_sess.get(Session, session_id)

    if role.upper() == 'ADMIN':
        ids = session.admins_ids
    elif role.upper() == 'PLAYER':
        ids = session.players_ids

    if action.upper() == 'ADD':
        if str(user_id) not in ids.split(';'):
            session.ids += ';' + str(user_id)
            db_sess.merge(session)
            db_sess.commit()
    elif action.upper() == 'DELETE':
        ids = ids.split(';')
        if str(user_id) in ids:
            ids.remove(str(user_id))
            ids = ';'.join(ids)
            db_sess.merge(session)
            db_sess.commit()


@sessions_api.route('/api/session_roles')
@login_required
def get_current_user_roles():
    db_sess = db_session.create_session()

    identifier = str(current_user.id)
    session_id = current_user.game_session_id
    session = db_sess.query(Session).filter(Session.id == session_id).first()
    roles = []
    if session:
        if identifier in str(session.admins_ids).split(';'):
            roles.append('Admin')
        if identifier in str(session.players_ids).split(';'):
            roles.append('Player')

    return jsonify(
        {
            "roles": roles
        }
    )


@sessions_api.route('/api/user_sessions')
@login_required
def get_current_user_sessions():
    db_sess = db_session.create_session()

    identifier = str(current_user.id)

    data = db_sess.query(Session).filter(or_(Session.admins_ids.contains(str(identifier)),
                                             Session.players_ids.contains(str(identifier)))).all()

    sessions = []
    for session_id in range(len(data)):
        if identifier in str(data[session_id].admins_ids) or \
                identifier in str(data[session_id].players):
            sessions.append(data[session_id])

    return jsonify(
        {
            'sessions':
                [item.to_dict(only=('id', 'title', 'admins_ids', 'players_ids'))
                 for item in sessions]
        }
    )
