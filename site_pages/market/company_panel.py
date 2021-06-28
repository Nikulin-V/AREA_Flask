#  Nikulin Vasily (c) 2021

#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.companies import Company
from data.functions import get_constant, get_game_roles, get_session_id
from data.sessions import Session
from data.stocks import Stock
from data.users import User
from forms.company_admin_management import CompanyAdminManagementForm
from tools import use_subdomains

company_panel_page = Blueprint('company-panel', __name__)
app = company_panel_page


# noinspection PyArgumentList
@app.route('/company-panel', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}company-panel.html')
@login_required
def company_panel(template, subdomain='market'):
    if 'Admin' not in get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    form = CompanyAdminManagementForm()
    message = ''

    evaluate_form(form)

    if form.validate_on_submit() or form.action.data == 'Удалить все компании':
        if form.action.data == 'Открыть компанию':
            if form.title.data and form.user_submitted and form.authors.data:
                company = Company(
                    session_id=get_session_id(),
                    title=form.title.data,
                    sector=form.new_sector.data,
                    authors_ids=', '.join(map(str, form.authors.data))
                )
                db_sess.add(company)
                db_sess.commit()
                for i in form.authors.data:
                    stocks = Stock(
                        session_id=get_session_id(),
                        user_id=i,
                        company_id=company.id,
                        stocks=get_constant('START_STOCKS')
                    )
                    db_sess.add(stocks)
                db_sess.commit()
                evaluate_form(form)
                message = 'Компания добавлена'
        elif form.action.data == 'Закрыть компанию':
            if form.company.data and form.user_submitted:
                company = form.company.data
                sector = form.sector.data
                company = db_sess.query(Company).filter(
                    Company.session_id == get_session_id(),
                    Company.title == company,
                    Company.sector == sector
                ).first()
                if company:
                    db_sess.delete(company)
                    db_sess.commit()
                    evaluate_form(form)
                    message = 'Компания удалена'
                else:
                    message = 'Компания с указанными данными не существует'
        elif form.action.data == 'Изменить компанию':
            if form.company.data and form.user_submitted:
                company = form.company.data
                sector = form.sector.data
                company = db_sess.query(Company).filter(
                    Company.session_id == get_session_id(),
                    Company.title == company,
                    Company.sector == sector
                ).first()
                if company:
                    if form.new_sector.data:
                        company.sector = form.new_sector.data
                    if form.title.data:
                        company.title = form.title.data
                    new_users = set(set(map(str, form.authors.data))
                                    ).difference(map(str, company.authors_ids.split(', ')))
                    if form.authors.data:
                        company.authors_ids = ', '.join(map(str, form.authors.data))
                    for i in new_users:
                        stocks = Stock(
                            session_id=get_session_id(),
                            user_id=i,
                            company_id=company.id,
                            stocks=get_constant('START_STOCKS')
                        )
                        db_sess.add(stocks)
                    db_sess.commit()
                    db_sess.merge(company)
                    db_sess.commit()
                    message = 'Компания изменена'
                    evaluate_form(form)
                else:
                    message = 'Компания с указанными данными не существует'
        elif form.action.data == 'Удалить все компании':
            if form.user_submitted and form.accept_delete_all_companies.data:
                companies = list(db_sess.query(Company).
                                 filter(Company.session_id == get_session_id()))
                for company in companies:
                    db_sess.delete(company)
                db_sess.commit()
                message = 'Все компании удалены'

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Панель управления компаниями',
                           message=message,
                           form=form)


def evaluate_form(form):
    db_sess = db_session.create_session()
    sectors = list(map(lambda x: x[0], set(db_sess.query(Company.sector).
                                           filter(Company.session_id == get_session_id()))))
    sectors.sort()

    players_ids = db_sess.query(Session.players_ids).filter(Session.players_ids == get_session_id())
    users = []
    for identifier in players_ids:
        users += list(map(lambda x: (x[3], f'{x[0]} {x[1]} | {x[2]}'),
                          db_sess.query(User.surname, User.name, User.email, User.id).
                          get(identifier)))
    form.authors.choices = users

    form.sector.choices = sectors
    if not form.sector.data or form.sector.data not in sectors:
        form.sector.data = sectors[0]

    companies = list(map(lambda x: x[0], db_sess.query(Company.title).filter(
        Company.sector == form.sector.data,
        Company.session_id == get_session_id()
    )))
    companies.sort()
    form.company.choices = companies
    if form.action.data in ['Закрыть компанию', 'Изменить компанию']:
        if not form.company.data:
            form.user_submitted = 0
            form.company.data = companies[0]
        else:
            form.user_submitted = 1

    if form.action.data == 'Открыть компанию':
        form.company.data = form.company.choices[0]
        if not form.title.data:
            form.user_submitted = 0
        else:
            form.user_submitted = 1
        if not form.new_sector.data:
            form.user_submitted = 0
        else:
            form.user_submitted = 1
    elif form.action.data == 'Изменить компанию':
        if not form.title.data:
            form.user_submitted = 0
            form.title.data = form.company.data
        else:
            form.user_submitted = 1
        if not form.new_sector.data:
            form.user_submitted = 0
            form.new_sector.data = form.sector.data
        else:
            form.user_submitted = 1
    elif form.action.data == 'Удалить все компании':
        form.user_submitted = 1
