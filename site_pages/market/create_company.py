#  Nikulin Vasily (c) 2021
from datetime import datetime

from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.companies import Company
from data.functions import get_game_roles, get_session_id, get_constant
from data.news import News
from data.wallets import Wallet
from forms.my_company_management import CompanyManagementForm
from tools import generate_string

my_companies_page = Blueprint('my-companies', __name__)
app = my_companies_page


# TODO: Удаление и изменение компаний через голосование
@app.route('/create-company', methods=['GET', 'POST'], subdomain='market')
@mobile_template('market/{mobile/}create-company.html')
@login_required
def my_companies(template):
    if not get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    # companies = [db_sess.query(Company.title, Company.id).get(identifier)
    #              for identifier in get_user_companies_ids(current_user.id)]

    form = CompanyManagementForm()
    message = ''
    new_company_fee = get_constant('NEW_COMPANY_FEE')

    if form.validate_on_submit():
        if form.sector.data and form.title.data:
            # f = request.files[]
            identifier = generate_string(db_sess.query(Company.id))
            company = Company(
                id=identifier,
                session_id=str(get_session_id()),
                title=form.title.data,
                description=form.description.data if form.description.data else '',
                sector=form.sector.data,
                # TODO: company logo upload
                # logo_url=form.logo_url.data
            )
            news = News(
                session_id=get_session_id(),
                title=f'Новая компания: {form.title.data} !',
                message=form.description.data,
                user_id=current_user.id,
                company_id=identifier,
                date=datetime.now(),
                author=f'от лица компании "{form.title.data}"',
                # picture=form.logo.data
            )
            wallet = db_sess.query(Wallet).filter(
                Wallet.user_id == current_user.id,
                Wallet.session_id == get_session_id()
            ).first()
            if not wallet.money:
                wallet = Wallet(
                    session_id=get_session_id(),
                    user_id=current_user.id,
                    money=get_constant('START_WALLET_MONEY')
                )
                db_sess.add(wallet)
                db_sess.commit()
            if wallet.money >= new_company_fee:
                wallet.money -= new_company_fee
                # f.save(secure_filename(f.filename))
                db_sess.add(company)
                db_sess.add(news)
                db_sess.merge(wallet)
                db_sess.commit()
                message = 'Компания создана'
            else:
                message = 'Недостаточно средств'

        # elif form.action.data == 'Закрыть компанию' and form.accept.data:
        #     identifier = form.company.data.split(' | ')[1]
        #     company = db_sess.query(Company).get(identifier)
        #     db_sess.delete(company)
        #
        #     offers = db_sess.query(Offer).filter(
        #         Offer.company_id == identifier,
        #         Offer.session_id == get_session_id()
        #     )
        #     for offer in offers:
        #         db_sess.delete(offer)
        #
        #     stocks = db_sess.query(Stock).filter(
        #         Stock.company_id == identifier,
        #         Stock.session_id == get_session_id()
        #     )
        #     for stock in stocks:
        #         db_sess.delete(stock)
        #
        #     news = News(
        #             session_id=get_session_id(),
        #             title=f'Компания закрывается: {company.title}',
        #             message='Все акции этой компании больше не являются действительными',
        #             user_id=current_user.id,
        #             company_id=identifier,
        #             date=datetime.now(),
        #             author=f'от лица компании "{company.title}"'
        #         )
        #     db_sess.add(news)
        #     db_sess.commit()
        #     message = 'Компания закрыта'
        #
        # elif form.action.data == 'Изменить компанию':
        #     pass

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Открыть компанию',
                           new_company_fee=new_company_fee,
                           message=message,
                           form=form)

# def get_user_companies_ids(user_id):
#     db_sess = db_session.create_session()
#     offer_company_ids = list(map(lambda x: x[0], db_sess.query(Offer.company_id).filter(
#         Offer.user_id == user_id,
#         Offer.session_id == get_session_id()
#     )))
#     stocks_company_ids = list(map(lambda x: x[0], db_sess.query(Stock.company_id).filter(
#         Stock.user_id == user_id,
#         Stock.session_id == get_session_id()
#     )))
#     return set(offer_company_ids + stocks_company_ids)
