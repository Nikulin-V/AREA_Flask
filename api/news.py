#  Nikulin Vasily © 2021
import datetime

from flask_login import current_user, login_required

from api import sock, api
from config import NEWS_PER_PAGE
from data import db_session
from data.functions import get_session_id, get_company_title, get_company_id
from data.news import News
from data.sessions import Session
from data.users import User
from tools.tools import send_response, fillJson


@sock.on('getNews')
@api.route('/api/news', methods=['GET'])
@login_required
def getNews(json=None):
    if json is None:
        json = dict()
    event_name = 'getNews'
    fillJson(json, ['page'])

    try:
        if json['page'] is None:
            page = 0
        else:
            page = int(json['page'])
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Page number must be integer']
            }
        )

    db_sess = db_session.create_session()

    news = db_sess.query(News).order_by(News.date.desc()).filter(
        News.session_id == get_session_id()).all()
    end = True if len(news) <= (page + 1) * NEWS_PER_PAGE else False
    is_liked = str(current_user.id) in news.liked_ids.split(";")
    news = news[page * NEWS_PER_PAGE:(page + 1) * NEWS_PER_PAGE]
    if not news:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Page number must be integer']
            }
        )
    n: News
    return send_response(
        event_name,
        {
            'message': 'Success',
            'news':
                [
                    {
                        'id': n.id,
                        'author': n.author if n.author != 'от себя'
                        else get_signature(n.user_id, n.company_id),
                        'title': n.title,
                        'message': n.message,
                        'date': n.date.strftime('%d %b at %H:%M'),
                        'picture': n.picture,
                        'likes': 0 if n.liked_ids is None
                        else len(str(n.liked_ids).split(';')),
                        'isLiked': is_liked,
                        'isMine': current_user.id == n.user_id
                    }
                    for n in news
                ],
            'end': end
        }
    )


@sock.on('createNews')
@api.route('/api/news', methods=['POST'])
@login_required
def createNews(json=None):
    if json is None:
        json = dict()

    event_name = 'createNews'
    fillJson(json, ['companyTitle', 'title', 'message', 'imageUrl'])

    if json['companyTitle'] is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify companyTitle']
            }
        )

    if json['companyTitle']:
        company_id = get_company_id(json['companyTitle'])
    else:
        company_id = None
    db_sess = db_session.create_session()

    if not current_user.game_session_id:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify game session']
            }
        )
    elif not json['title']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify title']
            }
        )

    news = News(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=company_id,
        title=json['title'],
        message=json['message'] or '',
        date=datetime.datetime.now(),
        author=get_signature(current_user.id, company_id),
        picture=json['imageUrl']
    )

    db_sess.add(news)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@sock.on('editNews')
@api.route('/api/news', methods=['PUT'])
@login_required
def editNews(json=None):
    if json is None:
        json = dict()

    event_name = 'editNews'
    fillJson(json, ['identifier', 'title', 'message', 'imageUrl', 'isLike'])

    db_sess = db_session.create_session()

    if not json['identifier']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify identifier']
            }
        )

    news = db_sess.query(News).get(json['identifier'])

    if news is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['News not found']
            }
        )

    admins_ids = str(db_sess.query(Session).get(news.session_id).admins_ids).split(';')

    if news.user_id != current_user.id and news.user_id not in admins_ids \
            and current_user.id != '7' and not json['isLike']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have permissions to edit this post.']
            }
        )
    elif json['isLike']:
        if news.liked_ids is None:
            news.liked_ids = ''
        news.liked_ids = str(news.liked_ids)
        if str(current_user.id) not in news.liked_ids.split(';'):
            liked_ids = [] if not news.liked_ids else news.liked_ids.split(';')
            likes = len(liked_ids) + 1
            news.liked_ids = ';'.join(liked_ids + [str(current_user.id)])
        else:
            liked_ids = news.liked_ids.split(';')
            likes = len(liked_ids) - 1
            liked_ids.remove(str(current_user.id))
            news.liked_ids = ';'.join(liked_ids)
        db_sess.merge(news)
        db_sess.commit()
        return send_response(
            event_name,
            {
                'message': 'Success',
                'likes': likes,
                'errors': []
            }
        )

    news.title = json['title'] or news.title
    news.message = news.title if json['message'] is None else json['message']
    news.picture = news.title if json['imageUrl'] is None else json['imageUrl']

    db_sess.merge(news)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@sock.on('deleteNews')
@api.route('/api/news', methods=['DELETE'])
@login_required
def deleteNews(json=None):
    if json is None:
        json = dict()

    event_name = 'deleteNews'
    fillJson(json, ['identifier'])

    db_sess = db_session.create_session()

    if not json['identifier']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify identifier']
            }
        )

    news = db_sess.query(News).get(json['identifier'])

    admins_ids = str(db_sess.query(Session).get(news.session_id).admins_ids).split(';')

    if news.user_id != current_user.id and news.user_id not in admins_ids and\
            current_user.id != '7':
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have permissions to delete this post.']
            }
        )

    db_sess.delete(news)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


def get_signature(user_id, company_id=None):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if company_id is None:
        return f'{user.surname} {user.name}'
    else:
        return f'{user.surname} {user.name} | <b>{get_company_title(company_id)}</b>'
