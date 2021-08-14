#  Nikulin Vasily © 2021
import os
from datetime import datetime

from flask_login import login_required, current_user

from api import api, sock
from config import sectors, icons
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
from tools.tools import fillJson, send_response, deposit_wallet
from tools.url import url


@sock.on('createCompany')
@api.route('/api/companies', methods=['POST'])
@login_required
def createCompany(json=None):
    if json is None:
        json = dict()
    event_name = 'createCompany'
    fillJson(json, ['sector', 'title', 'logoPath', 'description'])

    sector = json['sector']
    title = json['title']
    logoPath = json['logoPath']
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

    if (json['logoPath'] is not None) and \
            (not str(json['logoPath']).startswith(os.path.join("static", "images", "uploaded"))):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['File is unsafe or located on a foreign server']
            }
        )

    company = Company(
        session_id=get_session_id(),
        title=title,
        description=description if description else '',
        sector=sector,
        logo_url=logoPath if logoPath else ''
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
        picture=logoPath
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
        db_sess.commit()

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
        send_response(
            event_name,
            {
                'message': 'Success',
                'errors': []
            }
        )

        return send_response(
            'showNotifications',
            {
                'message': 'Success',
                'notifications': [
                    {
                        'logoSource': icons['new_company'],
                        'author': news.author.split(' | ')[0],
                        'company': None if len(news.author.split(' | ')) == 1
                        else news.author.split(' | ')[1],
                        'date': news.date.strftime('%d %B'),
                        'time': news.date.strftime('%H:%M'),
                        'redirectLink': f'{url("market.news")}#{news.id}'
                    }
                ],
                'errors': []
            },
            broadcast=True, include_self=False
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

    stocks = db_sess.query(Stock).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == company.id
    ).all() + db_sess.query(Offer).filter(
        Offer.session_id == get_session_id(),
        Offer.company_id == company.id
    ).all()

    all_stocks_count = sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == company.id
    ).all())) + sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
        Offer.session_id == get_session_id(),
        Offer.company_id == company.id
    ).all()))

    for stock in stocks:
        cashback = get_constant('NEW_COMPANY_FEE') * stock.stocks / all_stocks_count
        deposit_wallet(stock.user_id, cashback)

    delete_all_company_data(company.id)
    db_sess.delete(company)

    news = News(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=company.id,
        title=f'Компания закрывается: {company.title}',
        message='Все акции и новости компании были удалены.<br>'
                'Имущество компании было продано, а прибыль распределена между бывшими акционерами '
                'компании.',
        date=datetime.now(),
        author=f'<b>{company.title}</b>'
    )
    db_sess.add(news)
    db_sess.commit()

    return send_response(
        'showNotifications',
        {
            'message': 'Success',
            'notifications': [
                {
                    'logoSource': icons['close_company'],
                    'author': news.author.split(' | ')[0],
                    'company': None if len(news.author.split(' | ')) == 1
                    else news.author.split(' | ')[1],
                    'date': news.date.strftime('%d %B'),
                    'time': news.date.strftime('%H:%M'),
                    'redirectLink': f'{url("market.news")}#{news.id}'
                }
            ],
            'errors': []
        },
        broadcast=True, include_self=False
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
