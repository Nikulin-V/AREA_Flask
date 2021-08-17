#  Nikulin Vasily © 2021
import datetime

from flask_login import login_required, current_user

from config import icons
from data import db_session
from data.functions import get_session_id, get_company_id, get_company_title
from data.news import News
from data.offers import Offer
from data.scheduled_job import ScheduledJob
from data.stockholders_votes import SVote
from data.stocks import Stock
from market.api import api, socket
from market.api.companies import deleteCompanyAction
from tools.tools import is_stockholder, votes, is_voted, fillJson, send_response
from tools.url import url
from tools.words import morph


@socket.on('createStockholdersVoting')
@api.route('/api/svotes', methods=['POST'])
@login_required
def createStockholdersVoting(json=None):
    """
    Create session

    Required arguments:
        companyId or companyTitle
        action

    Args:
        json (dict of str): new stockholders voting data

    JSON Args:
        companyTitle (str): companyTitle
        companyId (str): company id
        action (str): voting action (releaseNewStocks or closeCompany)
        count (int): additional argument (depends on selected action)

    Returns:
        New voting's id (JSON)

    """
    if json is None:
        json = dict()

    event_name = 'createStockholdersVoting'
    fillJson(json, ['companyId', 'companyTitle', 'action', 'count'])

    companyId = json['companyId']
    companyTitle = json['companyTitle']
    action = json['action']
    count = json['count']

    actions = ['releaseNewStocks', 'closeCompany']
    actions_with_count = ['releaseNewStocks']

    try:
        count = int(count)
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Count must be an integer number']
            }
        )

    if not (companyId or companyTitle):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify id or title of company']
            }
        )
    elif action is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify the title of new session']
            }
        )
    elif action not in actions:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['There is no such action\nTip: releaseNewStocks, closeCompany']
            }
        )
    elif action in actions_with_count and (count is None or count < 1):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify the count of new stocks']
            }
        )

    if not companyId:
        companyId = get_company_id(companyTitle)

    if not is_stockholder(companyId):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You are not stockholder of this company']
            }
        )

    if action == 'closeCompany':
        action = 'Закрыть компанию'
    elif action == 'releaseNewStocks':
        if count % 10 <= 4:
            action = f'Выпустить по {count} акции на 1 существующую'
        else:
            action = f'Выпустить по {count} акций на 1 существующую'

    db_sess = db_session.create_session()

    voting = SVote(
        session_id=get_session_id(),
        company_id=companyId,
        action=action,
    )
    db_sess.add(voting)
    db_sess.commit()

    new_scheduled_job = ScheduledJob(
        model='SVote',
        object_id=voting.id,
        action='Delete',
        datetime=datetime.datetime.now() + datetime.timedelta(1)
    )
    db_sess.add(new_scheduled_job)
    db_sess.commit()

    send_response(
        event_name,
        {
            'message': 'Success',
            'errors': [],
            'data': {
                'id': voting.id
            }
        }
    )

    return send_response(
        'showNotifications',
        {
            'message': 'Success',
            'notifications': [
                {
                    'logoSource': icons['new_svoting'],
                    'company': get_company_title(companyId),
                    'author': voting.action,
                    'date': datetime.datetime.now().strftime('%d %B'),
                    'time': datetime.datetime.now().strftime('%H:%M'),
                    'redirectLink': f'{url("market.stockholders_voting")}#{voting.id}'
                }
            ],
            'errors': []
        },
        broadcast=True, include_self=False
    )


@socket.on('getStockholdersVotes')
@api.route('/api/svotes', methods=['GET'])
@login_required
def getStockholdersVotes():
    event_name = 'getStockholdersVotes'

    db_sess = db_session.create_session()

    session_id = get_session_id()
    if session_id is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': 'You are not in game session'
            }
        )

    data = db_sess.query(SVote).filter(SVote.session_id == session_id).all()
    v: SVote
    votings = [(v.id, get_company_title(v.company_id), v.action,
                votes(v.voted_stockholders_ids, v.company_id), is_voted(v.voted_stockholders_ids))
               for v in data if is_stockholder(v.company_id)]

    return send_response(
        event_name,
        {
            'message': 'Success',
            'votes':
                [
                    {
                        'id': v[0],
                        'company': v[1],
                        'action': v[2],
                        'votes': f'{v[3][0]}/{v[3][1]}',
                        'is_voted': v[4],
                    }
                    for v in votings
                ]
        }
    )


def release_new_stocks(voting, count):
    db_sess = db_session.create_session()
    stocks = db_sess.query(Stock).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == voting.company_id,
    ).all()
    s: Stock
    released_stocks_count = 0
    for s in stocks:
        released_stocks_count += s.stocks * count
        s.stocks += s.stocks * count
        db_sess.merge(s)

    offers = db_sess.query(Offer).filter(
        Offer.session_id == get_session_id(),
        Offer.company_id == voting.company_id
    ).all()
    of: Offer
    for of in offers:
        stocks = db_sess.query(Stock).filter(
            Stock.session_id == get_session_id(),
            Stock.company_id == of.company_id,
            Stock.user_id == of.user_id
        ).first()
        if stocks:
            stocks.stocks += of.stocks
            released_stocks_count += of.stocks
            db_sess.merge(stocks)
        else:
            new_stocks = Stock(
                session_id=of.session_id,
                company_id=of.company_id,
                user_id=of.user_id,
                stocks=of.stocks
            )
            db_sess.add(new_stocks)

    news = News(
        session_id=get_session_id(),
        user_id=None,
        company_id=voting.company_id,
        title=f'Эмиссия акций: {get_company_title(voting.company_id)}',
        message=f'Акционеры компании большинством голосов приняли решение о выпуске '
                f'{released_stocks_count} новых акций.',
        date=datetime.datetime.now(),
        author=f'<b>{get_company_title(voting.company_id)}</b>'
    )
    db_sess.add(news)
    db_sess.commit()
    send_response(
        'showNotifications',
        {
            'message': 'Success',
            'notifications': [
                {
                    'logoSource': icons['release_stocks'],
                    'company': news.author,
                    'author': str(released_stocks_count) + ' ' + morph.parse("акций")[
                        0].make_agree_with_number(released_stocks_count).word,
                    'date': news.date.strftime('%d %B'),
                    'time': news.date.strftime('%H:%M'),
                    'redirectLink': f'{url("market.marketplace")}#{news.id}'
                }
            ],
            'errors': []
        },
        broadcast=True, include_self=False
    )


def do_voting_action(voting):
    if voting.action == 'Закрыть компанию':
        deleteCompanyAction(companyId=voting.company_id)
    elif voting.action.startswith('Выпустить'):
        count = int(voting.action.split()[2])
        release_new_stocks(voting, count)


@socket.on('voteInStockholdersVoting')
@api.route('/api/svotes', methods=['PUT'])
@login_required
def voteInStockholdersVoting(json=None):
    if json is None:
        json = dict()
    event_name = 'voteInStockholdersVoting'
    fillJson(json, ['identifier'])

    identifier = json['identifier']

    db_sess = db_session.create_session()

    if identifier is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify id of voting']
            }
        )

    voting: SVote = db_sess.query(SVote).get(identifier)

    if voting is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Voting not found']
            }
        )

    if not is_stockholder(voting.company_id):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You are not stockholder of this company']
            }
        )

    if voting.voted_stockholders_ids is None:
        voted_stockholders_ids = []
    else:
        voted_stockholders_ids = str(voting.voted_stockholders_ids).split(';')
        while '' in voted_stockholders_ids:
            voted_stockholders_ids.remove('')

    if is_voted(voting.voted_stockholders_ids):
        voted_stockholders_ids.remove(str(current_user.id))
    else:
        voted_stockholders_ids.append(str(current_user.id))

        if is_votes_enough(db_sess, voting.company_id, voted_stockholders_ids):
            do_voting_action(voting)

            db_sess.delete(voting)

            scheduled_job = db_sess.query(ScheduledJob).filter(
                ScheduledJob.object_id == voting.id).all()
            for j in scheduled_job:
                db_sess.delete(j)

            db_sess.commit()
            return send_response(
                event_name,
                {
                    'message': 'Success',
                    'data': {'end': True},
                    'errors': []
                }
            )

    voting.voted_stockholders_ids = ';'.join(voted_stockholders_ids)

    db_sess.merge(voting)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'data': {'end': False},
            'errors': []
        }
    )


def is_votes_enough(db_sess, company_id, voted_stockholders_ids):
    all_stocks_count = sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == company_id
    )))
    # noinspection PyUnresolvedReferences
    voted_for_stocks = sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == company_id,
        Stock.user_id.in_(voted_stockholders_ids))
                               ))
    if voted_for_stocks > all_stocks_count / 2:
        return True
    return False
