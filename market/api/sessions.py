#  Nikulin Vasily © 2021

from flask_login import current_user, login_required

from config import default_constants
from data import db_session
from data.companies import Company
from data.config import Constant
from data.news import News
from data.offers import Offer
from data.sessions import Session
from data.stockholders_votes import SVote
from data.stocks import Stock
from data.users import User
from data.votes import Vote
from data.wallets import Wallet
from market.api import api, socket
from tools.tools import fillJson, send_response


@socket.on('getSessions')
@api.route('/api/sessions', methods=['GET'])
@login_required
def getSessions(json=None):
    """
    Get info about sessions

    Required arguments: -

    Args:
        json (dict of str):

    JSON Args:
        identifier (str): session's id

    Returns:
        Info about session/sessions (JSON)
    """

    if json is None:
        json = dict()

    event_name = 'getSessions'
    fillJson(json, ['identifier', 'title'])

    identifier = json['identifier']

    db_sess = db_session.create_session()

    if identifier:
        sessions = [db_sess.query(Session).get(identifier)]
    else:
        sessions = db_sess.query(Session).all()
        sessions = list(filter(lambda x: str(current_user.id) in str(x.players_ids).split(';'),
                               sessions))

    if not sessions:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': [f'The session with <id:{identifier}> not found']
            }
        )

    current_session = db_sess.query(Session).get(current_user.game_session_id)
    if current_session is None:
        current_session = sessions[0]
        user = db_sess.query(User).get(current_user.id)
        user.game_session_id = current_session.id
        db_sess.merge(user)
        db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'sessions':
                [item.to_dict(only=('id', 'title'))
                 for item in sessions],
            'currentSession':
                {
                    'id': current_session.id,
                    'title': current_session.title
                },
            'isAdmin': str(current_user.id) in str(current_session.admins_ids).split(';')
        }
    )


# noinspection PyArgumentList
@socket.on('createSession')
@api.route('/api/sessions', methods=['POST'])
@login_required
def createSession(json=None):
    """
    Create session

    Required arguments:
        title

    Args:
        json (dict of str): session's title

    Returns:
        New session's id (JSON)

    """
    if json is None:
        json = dict()

    event_name = 'createSession'
    fillJson(json, ['title'])

    title = json['title']

    if title is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify the title of new session']
            }
        )

    db_sess = db_session.create_session()

    if title in list(map(lambda x: x[0], db_sess.query(Session.title).all())):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['This title has taken.']
            }
        )

    session = Session(
        title=title,
        admins_ids=str(current_user.id),
        players_ids=str(current_user.id)
    )
    db_sess.add(session)
    db_sess.commit()

    constants = [
        Constant(
            session_id=session.id,
            name=constant_name,
            value=constant_value
        )
        for constant_name, constant_value in default_constants.items()
    ]

    db_sess.add_all(constants)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': [],
            'id': session.id
        }
    )


@socket.on('editSession')
@api.route('/api/sessions', methods=['PUT'])
@login_required
def editSession(json=None):
    if json is None:
        json = dict()
    """
    Edit session

    Required arguments: -

    Args:
        json (dict of str): dict of new user data

    Session data:
        title (string): title\n
        admins_ids (string): ';' separated ids of admins\n
        players_ids (string): ';'separated ids of players

    Returns:
        Success message (JSON)
    """

    event_name = 'editSession'
    fillJson(json, ['title', 'adminsIds', 'playersIds'])
    session_data = dict()

    for arg in json.keys():
        session_data[arg] = json[arg]

    db_sess = db_session.create_session()
    session_id = current_user.game_session_id
    session = db_sess.get(Session, session_id)
    session: Session

    if str(current_user.id) not in session.admins_ids:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You are not admin of current session']
            }
        )

    title = session_data['title']
    admins_ids = session_data['adminsIds']
    players_ids = session_data['playersIds']

    session.title = title if title else session.title
    session.admins_ids = admins_ids if admins_ids else session.admins_ids
    session.players_ids = players_ids if players_ids else session.players_ids

    db_sess.merge(session)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@socket.on('deleteSession')
@api.route('/api/sessions', methods=['DELETE'])
@login_required
def deleteSession():
    """
    Delete current session with all its data

    Required arguments: -

    Returns:
        Success message (JSON)
    """

    event_name = 'deleteSession'

    db_sess = db_session.create_session()
    session_id = current_user.game_session_id
    if session_id is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have any sessions']
            }
        )

    session = db_sess.query(Session).get(session_id)
    session: Session

    if str(current_user.id) not in str(session.admins_ids):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You are not admin of current session']
            }
        )

    delete_all_session_data(session_id)
    db_sess.delete(session)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


def delete_all_session_data(session_id):
    """
    Delete all data of selected session

    Args:
        session_id (str): session id

    """
    db_sess = db_session.create_session()
    models = [Company, Offer, News, SVote, Stock, Vote, Wallet, Constant]
    items = []
    for model in models:
        items += list(db_sess.query(model).filter(model.session_id == session_id).all())
    for item in items:
        db_sess.delete(item)
    db_sess.commit()
