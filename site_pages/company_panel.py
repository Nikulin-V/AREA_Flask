#  Nikulin Vasily (c) 2021

#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.companies import Company
from data.config_constants import get_constant
from data.stocks import Stock
from data.users import User
from forms.company_management import CompanyManagementForm

company_panel_page = Blueprint('company-panel', __name__)
app = company_panel_page


# noinspection PyArgumentList
@app.route('/company-panel', methods=['GET', 'POST'])
@mobile_template('{mobile/}company-panel.html')
@login_required
def company_panel(template):
    if 'Админ' not in current_user.game_role:
        abort(404)

    db_sess = db_session.create_session()

    form = CompanyManagementForm()
    message = ''

    evaluate_form(form)

    if form.validate_on_submit() or form.action.data == 'Удалить все компании':
        if form.action.data == 'Добавить компанию':
            if form.title.data and form.user_submitted and form.authors.data:
                company = Company(
                    title=form.title.data,
                    section=form.new_section.data,
                    authors_ids=', '.join(map(str, form.authors.data))
                )
                db_sess.add(company)
                db_sess.commit()
                for i in form.authors.data:
                    stocks = Stock(
                        user_id=i,
                        company_id=company.id,
                        stocks=get_constant('START_STOCKS')
                    )
                    db_sess.add(stocks)
                db_sess.commit()
                evaluate_form(form)
                message = 'Компания добавлена'
        elif form.action.data == 'Удалить компанию':
            if form.company.data and form.user_submitted:
                company = form.company.data
                section = form.section.data
                company = db_sess.query(Company).filter(
                    Company.title == company,
                    Company.section == section
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
                section = form.section.data
                company = db_sess.query(Company).filter(
                    Company.title == company,
                    Company.section == section
                ).first()
                if company:
                    if form.new_section.data:
                        company.section = form.new_section.data
                    if form.title.data:
                        company.title = form.title.data
                    new_users = set(set(map(str, form.authors.data))
                                    ).difference(map(str, company.authors_ids.split(', ')))
                    if form.authors.data:
                        company.authors_ids = ', '.join(map(str, form.authors.data))
                    for i in new_users:
                        stocks = Stock(
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
                companies = list(db_sess.query(Company))
                for company in companies:
                    db_sess.delete(company)
                db_sess.commit()
                message = 'Все компании удалены'

    return render_template(template,
                           title='Панель управления компаниями',
                           message=message,
                           form=form)


def evaluate_form(form):
    db_sess = db_session.create_session()
    sections = list(map(lambda x: x[0], set(db_sess.query(Company.section))))
    sections.sort()

    users = list(map(lambda x: (x[3], f'{x[0]} {x[1]} | {x[2]}'),
                     db_sess.query(User.surname, User.name, User.email, User.id).filter(
                         User.game_role is not None
                     )))
    form.authors.choices = users

    form.section.choices = sections
    if not form.section.data or form.section.data not in sections:
        form.section.data = sections[0]

    companies = list(map(lambda x: x[0], db_sess.query(Company.title).filter(
        Company.section == form.section.data
    )))
    companies.sort()
    form.company.choices = companies
    if form.action.data in ['Удалить компанию', 'Изменить компанию']:
        if not form.company.data:
            form.user_submitted = 0
            form.company.data = companies[0]
        else:
            form.user_submitted = 1

    if form.action.data == 'Добавить компанию':
        form.company.data = form.company.choices[0]
        if not form.title.data:
            form.user_submitted = 0
        else:
            form.user_submitted = 1
        if not form.new_section.data:
            form.user_submitted = 0
        else:
            form.user_submitted = 1
    elif form.action.data == 'Изменить компанию':
        if not form.title.data:
            form.user_submitted = 0
            form.title.data = form.company.data
        else:
            form.user_submitted = 1
        if not form.new_section.data:
            form.user_submitted = 0
            form.new_section.data = form.section.data
        else:
            form.user_submitted = 1
    elif form.action.data == 'Удалить все компании':
        form.user_submitted = 1
