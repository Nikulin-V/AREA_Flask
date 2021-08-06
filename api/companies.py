#  Nikulin Vasily © 2021
from datetime import datetime

from flask_login import login_required, current_user

from api import api, sock
from config import sectors
from data import db_session
from data.companies import Company
from data.db_functions import get_session_id
from data.functions import get_company_id, get_constant
from data.news import News
from data.offers import Offer
from data.stockholders_votes import SVote
from data.stocks import Stock
from data.votes import Vote
from data.wallets import Wallet
from tools.tools import fillJson, send_response


@sock.on('createCompany')
@api.route('/api/companies', methods=['POST'])
@login_required
def createCompany(json=None):
    if json is None:
        json = dict()
    event_name = 'createCompany'
    fillJson(json, ['sector', 'title', 'logoUrl', 'description'])

    sector = json['sector']
    title = json['title']
    logoUrl = json['logoUrl']
    description = json['description']

    if not sector or sector not in sectors:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify the sector of company']
            }
        )
    elif not title:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify the title of company']
            }
        )

    title = title.strip()

    db_sess = db_session.create_session()

    companies_titles = list(map(lambda x: x[0], db_sess.query(Company.title).filter(
        Company.session_id == get_session_id()).all()))
    if title in companies_titles:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['This title is already taken']
            }
        )

    company = Company(
        session_id=get_session_id(),
        title=title,
        description=description if description else '',
        sector=sector,
        logo_url=logoUrl if logoUrl else ''
    )
    db_sess.add(company)
    db_sess.commit()
    news = News(
        session_id=get_session_id(),
        title=f'Новая компания: {title}',
        message=description,
        user_id=current_user.id,
        company_id=company.id,
        date=datetime.now(),
        author=f'<b>{title}</b>',
        picture=logoUrl
    )
    db_sess.add(news)
    wallet = db_sess.query(Wallet).filter(
        Wallet.user_id == current_user.id,
        Wallet.session_id == get_session_id()
    ).first()
    stock = Stock(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=company.id,
        stocks=get_constant('START_STOCKS')
    )
    db_sess.add(stock)

    if wallet.money is None:
        wallet = Wallet(
            session_id=get_session_id(),
            user_id=current_user.id,
            money=get_constant('START_WALLET_MONEY')
        )
        db_sess.add(wallet)

    new_company_fee = get_constant('NEW_COMPANY_FEE')
    if wallet.money < new_company_fee:
        db_sess.rollback()
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have enough money']
            }
        )
    else:
        wallet.money -= new_company_fee
        db_sess.merge(wallet)
        db_sess.commit()
        return send_response(
            event_name,
            {
                'message': 'Success',
                'errors': []
            }
        )


@sock.on('getCompanies')
@api.route('/api/companies', methods=['GET'])
@login_required
def getCompanies():
    event_name = 'getCompanies'

    db_sess = db_session.create_session()
    companies = db_sess.query(Company).filter(Company.session_id == get_session_id()).all()
    c: Company
    response = {
        'message': 'Success',
        'companies': {s: [] for s in sectors}
    }

    for c in companies:
        response['companies'][c.sector].append(c.title)

    for s in sectors:
        response['companies'][s].sort()

    return send_response(event_name, response)


def deleteCompanyAction(event_name=None, companyId=None, companyTitle=None):
    if companyId is None and companyTitle is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify id or title of company']
            }
        )
    if companyId is None:
        companyId = get_company_id(companyTitle)

    db_sess = db_session.create_session()

    company = db_sess.query(Company).get(companyId)

    if company is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Company not found']
            }
        )

    companyTitle = company.title

    delete_all_company_data(companyId)
    db_sess.delete(company)

    news = News(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=companyId,
        title=f'Компания закрывается: {companyTitle}',
        message='Все акции и новости компании были удалены.',
        date=datetime.now(),
        author=f'<b>{companyTitle}</b>'
    )
    db_sess.add(news)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': [],
        }
    )


@sock.on('deleteCompany')
@api.route('/api/companies', methods=['DELETE'])
@login_required
def deleteCompany(json=None):
    if json is None:
        json = dict()
    event_name = 'deleteCompany'
    fillJson(json, ['companyId', 'companyTitle'])

    companyId = json['companyId']
    companyTitle = json['companyTitle']

    deleteCompanyAction(event_name, companyId, companyTitle)


def delete_all_company_data(company_id):
    db_sess = db_session.create_session()
    models = [Offer, News, SVote, Stock, Vote]
    items = []
    for model in models:
        items += list(db_sess.query(model).filter(model.company_id == company_id).all())
    for item in items:
        db_sess.delete(item)
    db_sess.commit()
