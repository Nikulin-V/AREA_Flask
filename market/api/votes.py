#  Nikulin Vasily © 2021
from flask_login import login_required, current_user

from config import sectors
from data import db_session
from data.companies import Company
from data.functions import get_session_id, get_company_id
from data.votes import Vote
from market.api import api, socket
from tools.tools import is_stockholder, fillJson, send_response


@socket.on('getCompaniesVotes')
@api.route('/api/votes', methods=['GET'])
@login_required
def getCompaniesVotes():
    event_name = 'getCompaniesVotes'

    db_sess = db_session.create_session()

    companies_ids = list(
        map(lambda x: x[0],
            db_sess.query(Company.id).filter(Company.session_id == get_session_id()).all()))
    response = {
        'message': 'Success',
        'votes': {s: [] for s in sectors},
        'errors': []
    }
    for companyId in companies_ids:
        company = db_sess.query(Company).get(companyId)
        response['votes'][company.sector].append({
            'company': company.title,
            'points': sum(map(lambda x: x[0], db_sess.query(Vote.points).filter(
                Vote.session_id == get_session_id(),
                Vote.company_id == companyId
            ).all())),
            'user_points': sum(map(lambda x: x[0], db_sess.query(Vote.points).filter(
                Vote.session_id == get_session_id(),
                Vote.company_id == companyId,
                Vote.user_id == current_user.id
            )))
        })

    return send_response(event_name, response)


@socket.on('voteInCompaniesVoting')
@api.route('/api/votes', methods=['PUT'])
@login_required
def voteInCompaniesVoting(json=None):
    if json is None:
        json = dict()
    event_name = 'voteInCompaniesVoting'
    fillJson(json, ['companyId', 'companyTitle', 'points'])

    companyId = json['companyId']
    companyTitle = json['companyTitle']
    points = json['points']

    db_sess = db_session.create_session()

    if companyId is None and companyTitle is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify id or title of company']
            }
        )

    if not companyId:
        companyId = get_company_id(companyTitle)

    if points is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify points for company']
            }
        )

    try:
        points = int(points)
        if points < 0:
            raise ValueError
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Points must be an integer number']
            }
        )

    if is_stockholder(companyId):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You are stockholder of this company']
            }
        )

    used_points = sum(map(lambda x: x[0], db_sess.query(Vote.points).filter(
        Vote.session_id == get_session_id(),
        Vote.user_id == current_user.id
    ).all())) - \
                  sum(map(lambda x: x[0], db_sess.query(Vote.points).filter(
                      Vote.session_id == get_session_id(),
                      Vote.company_id == companyId,
                      Vote.user_id == current_user.id
                  )))

    if used_points + points > 100:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'data': {
                    'points': 100 - used_points
                },
                'errors': ['You do not have enough points']
            }
        )

    votings = db_sess.query(Vote).filter(
        Vote.session_id == get_session_id(),
        Vote.company_id == companyId,
        Vote.user_id
    ).all()

    for v in votings:
        db_sess.delete(v)
    db_sess.commit()

    voting: Vote = Vote(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=companyId,
        points=points
    )

    db_sess.add(voting)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )
