#  Nikulin Vasily (c) 2021

from flask import render_template, Blueprint
from flask_login import current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.companies import Company
from data.news import News
from data.users import User

my_news_page = Blueprint('my-news-page', __name__)
app = my_news_page


@app.route('/my-news')
@mobile_template('{mobile/}my-news.html')
def my_news(template):
    db_sess = db_session.create_session()

    data = list(db_sess.query(
        News.title, News.message, News.user_id, News.company_id, News.date).filter(
        User.id == current_user.id)
    )
    news_list = []
    days_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
                 'сентября', 'октября', 'ноября', 'декабря']

    for i in range(len(data)):
        user = ' '.join(db_sess.query(User.surname, User.name).filter(
            User.id == data[i][2]
        ).first())
        company = db_sess.query(Company.title).filter(
            Company.id == data[i][3]
        ).first()[0]
        date = str(data[i][4]).split()
        time = date[1].split(':')
        time = ':'.join((time[0], time[1]))
        date = date[0].split('-')
        date = f'{date[2]} {days_list[int(date[1]) - 1]}'
        datetime = f'{date} в {time}'
        news_list.append([data[i][0], data[i][1], user, company, datetime])

    return render_template(template,
                           title='Мои новости', news=news_list)
