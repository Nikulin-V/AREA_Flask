#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.companies import Company
from data.votes import Vote
from forms.vote import VoteForm
from data.functions import evaluate_form, get_company_id, get_game_roles, get_session_id

voting_page = Blueprint('companies-voting', __name__)
app = voting_page


@app.route('/voting', methods=['GET', 'POST'])
@mobile_template('{mobile/}voting.html')
@login_required
def companies_voting(template):
    db_sess = db_session.create_session()

    form = VoteForm()

    message = ''

    # self company
    company = db_sess.query(Company.id, Company.title). \
        filter(Company.authors_ids.contains(str(current_user.id)),
               Company.session_id == get_session_id()).first()
    if company:
        points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                              filter(Vote.company_id == company[0],
                                     Vote.session_id == get_session_id()))))
        company = list(company) + [points]

    if form.is_submitted():
        if form.points.data is None:
            pass
        elif form.company.data == company[1]:
            message = 'Вы не можете голосовать за свой проект'
        elif 0 < form.points.data <= 100:
            company_id = db_sess.query(Company.id). \
                filter(Company.title == form.company.data,
                       Company.session_id == get_session_id()).first()[0]
            current_voted_points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                                filter(
                Vote.user_id == current_user.id,
                Vote.session_id == get_session_id()
            ))))
            current_company_voted_points = db_sess.query(Vote.points). \
                filter(Vote.user_id == current_user.id,
                       Vote.company_id == company_id,
                       Vote.session_id == get_session_id()).first()
            if current_company_voted_points:
                current_company_voted_points = current_company_voted_points[0]
            else:
                current_company_voted_points = 0
            if current_voted_points + form.points.data <= 100 or \
                    current_company_voted_points >= form.points.data or \
                    (current_company_voted_points < form.points.data and
                     current_voted_points - current_company_voted_points + form.points.data <= 100):
                company_id = db_sess.query(Company.id). \
                    filter(Company.title == form.company.data,
                           Company.session_id == get_session_id()).first()
                if company_id:
                    company_id = company_id[0]
                vote = db_sess.query(Vote).filter(Vote.user_id == current_user.id,
                                                  Vote.company_id == company_id,
                                                  Vote.session_id == get_session_id()).first()
                if vote:
                    vote.points = form.points.data
                    db_sess.merge(vote)
                else:
                    vote = Vote(
                        session_id=get_session_id(),
                        user_id=current_user.id,
                        company_id=company_id,
                        points=form.points.data
                    )
                    db_sess.add(vote)
                db_sess.commit()
            else:
                message = f'Вам не хватает очков.\n' \
                          f'Вы можете отменить голос, назначив проекту 0 очков.\n' \
                          f'Ваши очки: {100 - current_voted_points}/100'
        elif form.points.data == 0:
            company_id = get_company_id(form.company.data)
            vote = db_sess.query(Vote).filter(Vote.user_id == current_user.id,
                                              Vote.company_id == company_id,
                                              Vote.session_id == get_session_id()).first()
            if vote:
                db_sess.delete(vote)
                db_sess.commit()
        else:
            message = 'Неверное число очков'

    sections, companies = evaluate_form(form)

    if not form.company.data and form.company.choices:
        form.company.data = form.company.choices[0]
    company_id = db_sess.query(Company.id).filter(Company.title == form.company.data,
                                                  Company.section == form.section.data,
                                                  Company.session_id == get_session_id()).first()
    if company_id:
        company_id = company_id[0]
    elif form.company.choices:
        form.company.data = form.company.choices[0]
        company_id = db_sess.query(Company.id).filter(Company.title == form.company.data,
                                                      Company.section == form.section.data,
                                                      Company.session_id == get_session_id()
                                                      ).first()
        if company_id:
            company_id = company_id[0]

    current_voted_points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                        filter(Vote.company_id == company_id,
                                               Vote.user_id == current_user.id,
                                               Vote.session_id == get_session_id()))))

    form.points.data = current_voted_points if current_voted_points else 0

    return render_template(template,
                           game_role=get_game_roles(),
                           form=form,
                           title='Компании',
                           message=message,
                           company=company,
                           companies=companies,
                           sections=sections)
