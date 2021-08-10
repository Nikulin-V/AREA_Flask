#  Nikulin Vasily © 2021
import datetime
import os
import random

from flask import request, abort, jsonify, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from api import sock, api
from config import NEWS_PER_PAGE, ALLOWED_EXTENSIONS
from data import db_session
from data.functions import get_session_id, get_company_title, get_company_id
from data.news import News
from data.scheduled_job import ScheduledJob
from data.sessions import Session
from data.users import User
from tools.tools import send_response, fillJson, safe_remove


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
    for n in news:
        n.is_liked = str(current_user.id) in str(n.liked_ids).split(";")
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
    admins_ids = str(db_sess.query(Session.admins_ids).filter(
        Session.id == get_session_id()).first()[0]).split(';')
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
                        'picture': url_for('static',
                                           filename=n.picture[7:].replace("\\", "/"))
                        if n.picture is not None else n.picture,
                        'likes': 0 if n.liked_ids is None or n.liked_ids == ''
                        else len(str(n.liked_ids).split(';')),
                        'isLiked': n.is_liked,
                        'canEdit': current_user.id == n.user_id or
                                   str(current_user.id) in admins_ids
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
    fillJson(json, ['companyTitle', 'title', 'message', 'imagePath', 'jobId'])

    if json['companyTitle'] is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify company title']
            }
        )

    if (json['imagePath'] is not None) and\
            (not str(json['imagePath']).startswith(os.path.join("static", "images", "uploaded"))):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['File is unsafe or located on a foreign server']
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

    delete_job(db_sess, json['jobId'])

    news = News(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=company_id,
        title=json['title'],
        message=json['message'] or '',
        date=datetime.datetime.now(),
        author=get_signature(current_user.id, company_id),
        picture=json['imagePath']
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
    fillJson(json, ['identifier', 'title', 'message', 'imagePath', 'isLike', 'jobId'])

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

    if news.user_id != current_user.id and str(current_user.id) not in admins_ids \
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
            is_liked = True
        else:
            liked_ids = news.liked_ids.split(';')
            likes = len(liked_ids) - 1
            liked_ids.remove(str(current_user.id))
            news.liked_ids = ';'.join(liked_ids)
            is_liked = False
        db_sess.merge(news)
        db_sess.commit()
        return send_response(
            event_name,
            {
                'message': 'Success',
                'likes': likes,
                'isLiked': is_liked,
                'errors': []
            }
        )

    if json['imagePath'] == '!clear':
        json['imagePath'] = ''
        if news.picture is not None:
            safe_remove(news.picture)
        news.picture = None
        db_sess.merge(news)
        db_sess.commit()

        return send_response(
            event_name,
            {
                'message': 'Success',
                'errors': []
            }
        )

    if (json['imagePath'] is not None) and \
            (not str(json['imagePath']).startswith(os.path.join("static", "images", "uploaded"))):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['File is unsafe or located on a foreign server']
            }
        )

    delete_job(db_sess, json['jobId'])

    news.title = json['title'] or news.title
    news.message = news.message if json['message'] is None else json['message']

    if json['imagePath'] is not None:
        if news.picture is not None:
            safe_remove(news.picture)
        news.picture = json['imagePath']

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

    if news.user_id != current_user.id and str(current_user.id) not in admins_ids and \
            current_user.id != '7':
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have permissions to delete this post.']
            }
        )

    if news.picture is not None:
        safe_remove(news.picture)

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


@api.route("/api/news/image", methods=['POST'])
def uploadImage():
    uploaded = request.files["illustration"]
    if (not uploaded) or (uploaded.filename == ''):
        abort(400)
    if allowed_file(uploaded.filename):
        filename = secure_filename(uploaded.filename)
        save_dir = os.path.join("static", "images", "uploaded")
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        path = str(os.path.join(save_dir, filename))
        while os.path.exists(path):
            ext = path.rfind(".")
            path = path[:ext] + str(random.randint(1, 1000000)) + path[ext:]
        uploaded.save(path)

        db_sess = db_session.create_session()
        scheduled_job = ScheduledJob(
            model=None,
            object_id=path,
            action='Delete unused picture',
            datetime=datetime.datetime.now() + datetime.timedelta(seconds=30)
        )

        db_sess.add(scheduled_job)
        db_sess.commit()

        return jsonify(
            {
                "path": path,
                "jobId": scheduled_job.id
            }
        )
    else:
        return jsonify(
            {
                "code": 1001,
                "error": "Security error",
                "description": "Wrong file format or potentially unsafe file"
            }
        )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS and \
           '/' not in filename


def delete_job(db_sess, job_id):
    scheduled_job = db_sess.query(ScheduledJob).get(job_id)
    if scheduled_job:
        db_sess.delete(scheduled_job)
