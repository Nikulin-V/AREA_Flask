#  Nikulin Vasily © 2021
import datetime

from flask_login import current_user, login_required

from api import api, sock
from data import db_session
from data.companies import Company
from data.functions import get_session_id, get_company_title, get_company_id, get_constant
from data.offers import Offer
from data.scheduled_job import ScheduledJob
from data.stocks import Stock
from data.votes import Vote
from data.wallets import Wallet
from tools.tools import fillJson, send_response


@sock.on('getOffers')
@api.route('/api/offers', methods=['GET'])
def getOffers():
    event_name = 'getOffers'

    db_sess = db_session.create_session()

    offers = db_sess.query(Offer).filter(
        Offer.session_id == get_session_id()
    ).all()
    offer: Offer
    offers.sort(key=lambda x: x.price)
    return send_response(
        event_name,
        {
            'message': 'Success',
            'offers':
                [
                    {
                        'id': offer.id,
                        'company': get_company_title(offer.company_id),
                        'stocks': offer.stocks,
                        'reserved_stocks': offer.reserved_stocks,
                        'price': offer.price,
                        'is_mine': offer.user_id == current_user.id,
                        'sector': db_sess.query(Company).get(offer.company_id).sector
                    }
                    for offer in offers]
        }
    )


@sock.on('createOffer')
@api.route('/api/offers', methods=['POST'])
@login_required
def createOffer(json=None):
    if json is None:
        json = dict()
    """Продать акции"""

    event_name = 'createOffer'
    fillJson(json, ['company', 'stocks', 'price'])

    company = json['company']
    stocks = json['stocks']
    price = json['price']

    if not (company and stocks and price):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify company, stocks count and price']
            }
        )

    try:
        company_id = get_company_id(company)
        stocks = int(stocks)
        price = int(price)
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Bad data types']
            }
        )

    db_sess = db_session.create_session()

    stock = db_sess.query(Stock).filter(
        Stock.session_id == get_session_id(),
        Stock.user_id == current_user.id,
        Stock.company_id == company_id,
        Stock.stocks >= stocks
    ).first()

    if not stock:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Stocks not found']
            }
        )

    if stock.stocks > stocks:
        stock.stocks -= stocks
        db_sess.merge(stock)
    else:
        db_sess.delete(stock)

    offer = Offer(
        session_id=get_session_id(),
        user_id=current_user.id,
        company_id=company_id,
        stocks=stocks,
        price=price
    )

    db_sess.add(offer)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@sock.on('editOffer')
@api.route('/api/offers', methods=['PUT'])
@login_required
def editOffer(json=None):
    if json is None:
        json = dict()
    """Купить акции"""
    event_name = 'editOffer'

    fillJson(json, ['company', 'stocks', 'isBuy', 'json'])

    company = json['company']
    stocks = json['stocks']
    isBuy = json['isBuy']
    chequeJson = json['json']

    if isBuy not in ['accept', 'decline']:
        if company is None:
            return send_response(
                event_name,
                {
                    'message': 'Error',
                    'errors': ['Specify the company']
                }
            )
        elif stocks is None:
            return send_response(
                event_name,
                {
                    'message': 'Error',
                    'errors': ['Specify the stocks count']
                }
            )
        stocks = int(stocks)

    db_sess = db_session.create_session()

    if isBuy == 'cheque':
        offers = db_sess.query(Offer).filter(
            Offer.session_id == get_session_id(),
            Offer.company_id == get_company_id(company),
            Offer.user_id != current_user.id,
            Offer.stocks - Offer.reserved_stocks > 0
        ).all()

        offers.sort(key=lambda x: x.price)

        cheque_offers = []
        scheduled_jobs_ids = []

        isEnough = True
        while stocks > 0:
            try:
                offer = offers.pop(0)
                curr_stocks = offer.stocks if offer.stocks <= stocks else stocks
                offer.reserved_stocks += curr_stocks
                scheduled_job = ScheduledJob(
                    model='Offer',
                    object_id=offer.id,
                    action=f'Undo {curr_stocks} stocks',
                    datetime=datetime.datetime.now() + datetime.timedelta(seconds=30)
                )
                scheduled_jobs_ids.append(scheduled_job.id)
                db_sess.add(scheduled_job)
                cheque_offers.append(
                    (offer.id, get_company_title(offer.company_id), curr_stocks, offer.price))
                stocks -= curr_stocks
                if stocks < 0:
                    stocks = 0
                db_sess.merge(offer)
            except IndexError:
                if cheque_offers:
                    isEnough = False
                    break
                else:
                    return send_response(
                        event_name,
                        {
                            'message': 'Error',
                            'errors': ['Not enough stocks']
                        }
                    )

        db_sess.commit()

        return send_response(
            event_name,
            {
                'message': 'Success',
                'offers':
                    [
                        {
                            'id': offer[0],
                            'company': offer[1],
                            'stocks': offer[2],
                            'price': offer[3],
                            'cost': offer[2] * offer[3]
                        }
                        for offer in cheque_offers],
                'isEnough': isEnough,
                'scheduledJobsIds': scheduled_jobs_ids
            }
        )
    elif isBuy == 'decline':
        delete_scheduled_jobs(chequeJson, db_sess)

        if chequeJson and 'offers' in chequeJson.keys():
            cheque = chequeJson['offers']

            for row in cheque:
                offer = db_sess.query(Offer).get(row['id'])
                offer.reserved_stocks -= int(row['stocks'])
                db_sess.merge(offer)

        db_sess.commit()

        return send_response(
            event_name,
            {
                'message': 'Success',
                'errors': []
            }
        )

    elif isBuy == 'accept':
        delete_scheduled_jobs(chequeJson, db_sess)

        cheque = json['json']['offers']

        first_cost = sum([int(row['price']) * int(row['stocks']) for row in cheque])

        customer_wallet = db_sess.query(Wallet).filter(
            Wallet.session_id == get_session_id(),
            Wallet.user_id == current_user.id
        ).first()

        company_id = get_company_id(cheque[0]['company'])

        all_stocks_count = sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
            Stock.session_id == get_session_id(),
            Stock.company_id == company_id
        ).all())) + sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
            Offer.session_id == get_session_id(),
            Offer.company_id == company_id
        ).all()))

        second_cost = 0
        for row in cheque:
            offer = db_sess.query(Offer).get(row['id'])

            stocks_get_profit = all_stocks_count - (
                sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                    Stock.session_id == get_session_id(),
                    Stock.company_id == company_id,
                    Stock.user_id.in_([current_user.id, offer.user_id])
                ))) + sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
                    Offer.session_id == get_session_id(),
                    Offer.company_id == company_id,
                    str(Stock.user_id).in_([current_user.id, offer.user_id])
                )))
            )

            second_cost += int(row['price']) * int(
                row['stocks']) * get_constant('FEE_FOR_STOCK') * stocks_get_profit

        if customer_wallet.money < first_cost + second_cost:
            return send_response(
                event_name,
                {
                    'message': 'Error',
                    'errors': ['You do not have enough money']
                }
            )

        # Снятие денег, получение акций и начисление комиссии
        for row in cheque:
            offer = db_sess.query(Offer).get(row['id'])

            stocks_get_profit = all_stocks_count - (
                    sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                        Stock.session_id == get_session_id(),
                        Stock.company_id == company_id,
                        str(Stock.user_id).in_([current_user.id, offer.user_id])
                    ))) + sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
                        Offer.session_id == get_session_id(),
                        Offer.company_id == company_id,
                        str(Stock.user_id).in_([current_user.id, offer.user_id])
                    )))
            )
            offer_first_cost = int(row['stocks']) * int(row['price'])
            offer_second_cost = offer_first_cost * stocks_get_profit * get_constant('FEE_FOR_STOCK')

            customer_wallet.money -= offer_first_cost + offer_second_cost

            seller_wallet = db_sess.query(Wallet).filter(
                Wallet.session_id == get_session_id(),
                Wallet.user_id == offer.user_id
            ).first()
            seller_wallet.money += offer_first_cost

            # Изменение количества акций на торговой площадке
            if offer.stocks <= int(row['stocks']):
                db_sess.delete(offer)
            else:
                offer.stocks -= int(row['stocks'])
                offer.reserved_stocks -= int(row['stocks'])
                db_sess.merge(offer)

            # Получение акций в инвентарь покупателя
            stock = db_sess.query(Stock).filter(
                Stock.session_id == get_session_id(),
                Stock.company_id == offer.company_id,
                Stock.user_id == current_user.id
            ).first()

            if not stock:
                stock = Stock(
                    session_id=get_session_id(),
                    user_id=current_user.id,
                    company_id=offer.company_id,
                    stocks=int(row['stocks'])
                )
                db_sess.add(stock)
            else:
                stock.stocks += int(row['stocks'])
                db_sess.merge(stock)

            # Начисление комиссии третьим лицам
            all_stocks = list(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                Stock.session_id == get_session_id(),
                Stock.company_id == company_id
            ).all())) + list(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
                Offer.session_id == get_session_id(),
                Offer.company_id == company_id
            ).all()))
            for stock in all_stocks:

                if str(stock.user_id) not in [current_user.id, offer.user_id]:
                    stockholder_wallet = db_sess.query(Wallet).filter(
                        Wallet.session_id == get_session_id(),
                        Wallet.user_id == stock.user_id
                    ).first()

                    fee = offer_first_cost * stock.stocks * get_constant('FEE_FOR_STOCK')

                    stockholder_wallet.money += fee
                    db_sess.merge(stockholder_wallet)

        deleteCompanyVotes(company_id, db_sess)
        db_sess.commit()

        return send_response(
            event_name,
            {
                'message': 'Success',
                'errors': []
            }
        )


@sock.on('deleteOffer')
@api.route('/api/offers', methods=['DELETE'])
@login_required
def deleteOffer(json=None):
    if json is None:
        json = dict()
    """Отменить продажу"""
    event_name = 'deleteOffer'

    fillJson(json, ['company', 'stocks', 'price'])

    company = json['company']
    stocks = json['stocks']
    price = json['price']

    if not (company and stocks and price):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify company, stocks and price of offer']
            }
        )

    try:
        stocks = int(stocks)
        price = int(price)
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Stocks and price must be integer']
            }
        )

    db_sess = db_session.create_session()

    offer = db_sess.query(Offer).filter(
        Offer.session_id == get_session_id(),
        Offer.company_id == get_company_id(company),
        Offer.stocks == stocks,
        Offer.price == price
    ).first()

    if not offer:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Offer not found']
            }
        )

    inv_stocks = db_sess.query(Stock).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == get_company_id(company),
        Stock.user_id == current_user.id
    ).first()

    if inv_stocks:
        inv_stocks.stocks += offer.stocks - offer.reserved_stocks
        db_sess.merge(inv_stocks)
    else:
        inv_stocks = Stock(
            session_id=get_session_id(),
            user_id=current_user.id,
            company_id=get_company_id(company),
            stocks=offer.stocks - offer.reserved_stocks,
        )
        db_sess.add(inv_stocks)

    if offer.reserved_stocks == 0:
        db_sess.delete(offer)
    else:
        offer.stocks = offer.reserved_stocks
        db_sess.merge(offer)

    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


def delete_scheduled_jobs(json, db_sess):
    if json and 'scheduledJobsIds' in json.keys():
        scheduled_jobs_ids = json['scheduledJobsIds']

        for scheduled_job_id in scheduled_jobs_ids:
            scheduled_job = db_sess.query(ScheduledJob).get(scheduled_job_id)
            if scheduled_job:
                db_sess.delete(scheduled_job)


def deleteCompanyVotes(company_id, db_sess):
    votes = db_sess.query(Vote).filter(
        Vote.session_id == get_session_id(),
        Vote.company_id == company_id,
        Vote.user_id == current_user.id
    ).all()

    for vote in votes:
        db_sess.delete(vote)

    db_sess.commit()
