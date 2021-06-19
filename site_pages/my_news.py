#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, abort
from flask_login import current_user
from flask_mobility.decorators import mobile_template

from datetime import datetime

from data import db_session
from data.companies import Company
from data.news import News
from data.offers import Offer
from data.stocks import Stock
from data.users import User
from forms.news_management import UserManagementForm

my_news_page = Blueprint('my-news', __name__)
app = my_news_page


@app.route('/my-news', methods=['GET', 'POST'])
@mobile_template('{mobile/}my-news.html')
def my_news(template):
    if 'Игрок' not in current_user.game_role:
        abort(404)
    db_sess = db_session.create_session()

    data = list(db_sess.query(News.title, News.message, News.company_id,
                              News.date, News.author, News.id,
                              News.picture).filter(
        News.user_id == current_user.id)
                    )
    news_list = []
    days_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
                 'сентября', 'октября', 'ноября', 'декабря']

    for i in range(len(data)):
        user = ' '.join(db_sess.query(User.surname, User.name).filter(
            User.id == current_user.id
        ).first())
        if data[i][4] == 'от себя':
            company = 0
        else:
            company = db_sess.query(Company.title).filter(
                Company.id == data[i][2]
            ).first()[0]
        date = str(data[i][3]).split()
        time = date[1].split(':')
        time = ':'.join((time[0], time[1]))
        date = date[0].split('-')
        date = f'{date[2]} {days_list[int(date[1]) - 1]}'
        date = f'{date} в {time}'
        news_list.append([data[i][5], data[i][0], data[i][1], user, company, date, data[i][4],
                          data[i][6]])

    form = UserManagementForm()
    message = ''

    if not form.action.data:
        form.action.data = 'Добавить новость'

    evaluate_form(form)

    if form.validate_on_submit() or form.is_submitted():
        if form.action.data == 'Добавить новость':
            if form.title.data and form.text.data and form.author.data:
                if form.author.data == 'от себя':
                    news = News(
                        title=form.title.data,
                        message=form.text.data,
                        user_id=current_user.id,
                        company_id=None,
                        date=datetime.now(),
                        author=form.author.data,
                        picture=form.picture.data
                    )
                else:
                    company = form.author.data.split('от лица компании ')[1]
                    news = News(
                        title=form.title.data,
                        message=form.text.data,
                        user_id=current_user.id,
                        company_id=db_sess.query(Company.id).filter(
                            Company.title == company.split('"')[1]
                        ).first()[0],
                        date=datetime.now(),
                        author=form.author.data,
                        picture=form.picture.data
                    )
                db_sess.add(news)
                db_sess.commit()
                evaluate_form(form)
                message = 'Новость добавлена'

                data = list(db_sess.query(News.title, News.message, News.company_id,
                                          News.date, News.author, News.id,
                                          News.picture).filter(
                    News.user_id == current_user.id)
                )
                news_list = []
                days_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
                             'августа', 'сентября', 'октября', 'ноября', 'декабря']

                for i in range(len(data)):
                    user = ' '.join(db_sess.query(User.surname, User.name).filter(
                        User.id == current_user.id
                    ).first())
                    if data[i][4] == 'от себя':
                        company = 0
                    else:
                        company = db_sess.query(Company.title).filter(
                            Company.id == data[i][2]
                        ).first()[0]
                    date = str(data[i][3]).split()
                    time = date[1].split(':')
                    time = ':'.join((time[0], time[1]))
                    date = date[0].split('-')
                    date = f'{date[2]} {days_list[int(date[1]) - 1]}'
                    date = f'{date} в {time}'
                    news_list.append(
                        [data[i][5], data[i][0], data[i][1], user, company, date, data[i][4],
                         data[i][6]])

        elif form.action.data == 'Удалить новость':
            identifier = db_sess.query(News.id).filter(
                News.user_id == current_user.id
            ).first()
            if identifier:
                identifier = form.identifier.data
                news = db_sess.query(News).filter(
                    News.id == identifier,
                ).first()
                if identifier:
                    if news:
                        if news.user_id == current_user.id or 'Админ' in current_user.game_role:
                            db_sess.delete(news)
                            db_sess.commit()
                            message = 'Новость удалена'
                            form.action.data = 'Добавить новость'

                            data = list(db_sess.query(News.title, News.message, News.company_id,
                                                      News.date, News.author, News.id,
                                                      News.picture).filter(
                                News.user_id == current_user.id)
                            )
                            news_list = []
                            days_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                                         'июля', 'августа', 'сентября', 'октября', 'ноября',
                                         'декабря']

                            for i in range(len(data)):
                                user = ' '.join(db_sess.query(User.surname, User.name).filter(
                                    User.id == current_user.id
                                ).first())
                                if data[i][4] == 'от себя':
                                    company = 0
                                else:
                                    company = db_sess.query(Company.title).filter(
                                        Company.id == data[i][2]
                                    ).first()[0]
                                date = str(data[i][3]).split()
                                time = date[1].split(':')
                                time = ':'.join((time[0], time[1]))
                                date = date[0].split('-')
                                date = f'{date[2]} {days_list[int(date[1]) - 1]}'
                                date = f'{date} в {time}'
                                news_list.append(
                                    [data[i][5], data[i][0], data[i][1], user, company, date,
                                     data[i][4],
                                     data[i][6]])

                        else:
                            message = 'Новость с указанным номером принадлежит другому пользователю'
                            form.action.data = 'Добавить новость'
                    else:
                        message = 'Новость с указанным номером отсутствует'
                        form.action.data = 'Добавить новость'
            else:
                message = 'У вас пока что нет новостей'
                form.action.data = 'Добавить новость'
        elif form.action.data == 'Изменить новость':
            identifier = db_sess.query(News.id).filter(
                News.user_id == current_user.id
            ).first()
            if identifier:
                identifier = form.identifier.data
                news = db_sess.query(News).filter(
                    News.id == identifier
                ).first()
                if identifier:
                    if news:
                        if news.user_id == current_user.id or 'Админ' in current_user.game_role:
                            if not form.title.data:
                                form.title.data = news.title
                                form.text.data = news.message
                                form.picture.data = news.picture
                                form.author.data = news.author
                            else:
                                news.title = form.title.data
                                news.message = form.text.data
                                news.author = form.author.data
                                if form.author.data == 'от себя':
                                    news.company_id = None
                                else:
                                    company = form.author.data.split('от лица компании ')[1]
                                    news.company_id = db_sess.query(Company.id).filter(
                                        Company.title == company.split('"')[1]
                                    ).first()[0]
                                news.picture = form.picture.data
                                news.date = datetime.now()
                                db_sess.merge(news)
                                db_sess.commit()
                                message = 'Новость изменена'
                                form.action.data = 'Добавить новость'
                                data = list(db_sess.query(News.title, News.message, News.company_id,
                                                          News.date, News.author, News.id,
                                                          News.picture).filter(
                                    News.user_id == current_user.id)
                                )
                                news_list = []
                                days_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                                             'июля', 'августа', 'сентября', 'октября', 'ноября',
                                             'декабря']
                                for i in range(len(data)):
                                    user = ' '.join(db_sess.query(User.surname, User.name).filter(
                                        User.id == current_user.id
                                    ).first())
                                    if data[i][4] == 'от себя':
                                        company = 0
                                    else:
                                        company = db_sess.query(Company.title).filter(
                                            Company.id == data[i][2]
                                        ).first()[0]
                                    date = str(data[i][3]).split()
                                    time = date[1].split(':')
                                    time = ':'.join((time[0], time[1]))
                                    date = date[0].split('-')
                                    date = f'{date[2]} {days_list[int(date[1]) - 1]}'
                                    date = f'{date} в {time}'
                                    news_list.append(
                                        [data[i][5], data[i][0], data[i][1], user, company, date,
                                         data[i][4],
                                         data[i][6]])
                        else:
                            message = 'Новость с указанным номером принадлежит другому пользователю'
                            form.action.data = 'Добавить новость'

                    else:
                        message = 'Новость с указанными данными отсутствует'
                        form.action.data = 'Добавить новость'
            else:
                message = 'У вас пока что нет новостей'
                form.action.data = 'Добавить новость'
    news_list.reverse()
    return render_template(template,
                           title='Мои новости',
                           message=message,
                           form=form,
                           news=news_list)


def evaluate_form(form):
    if form.author:
        db_sess = db_session.create_session()
        authors = ['от себя']
        companies_ids = get_user_companies(current_user.id)
        for company_id in companies_ids:
            company = db_sess.query(Company.title).filter(
                Company.id == company_id
            ).first()[0]
            authors.append(f'от лица компании "{str(company)}"')
        form.author.choices = authors
        if not form.author.data:
            form.author.default = form.author.choices[0]


def get_user_companies(user_id):
    db_sess = db_session.create_session()
    offer_company_ids = list(map(lambda x: x[0], db_sess.query(Offer.company_id).filter(
        Offer.user_id == user_id
    )))
    stocks_company_ids = list(map(lambda x: x[0], db_sess.query(Stock.company_id).filter(
        Stock.user_id == user_id
    )))
    return offer_company_ids + stocks_company_ids
