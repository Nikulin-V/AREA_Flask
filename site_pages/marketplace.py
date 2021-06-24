#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.functions import get_game_roles, get_constant, get_session_id
from data.offers import Offer
from data.stocks import Stock
from data.transactions import Transaction
from data.users import User
from data.wallets import Wallet
from forms.purchase import PurchaseForm
from forms.stocks import StocksForm
from data.functions import evaluate_form, update_market_info, get_company_id, \
    get_company_title

marketplace_page = Blueprint('marketplace', __name__)
app = marketplace_page


@app.route('/marketplace', methods=['GET', 'POST'])
@mobile_template('{mobile/}marketplace.html')
@login_required
def marketplace(template):
    if not get_game_roles():
        abort(404)

    if not get_constant('GAME_RUN'):
        return redirect('/game-result')
    db_sess = db_session.create_session()

    form = StocksForm()
    purchase = PurchaseForm()

    evaluate_form(form)

    message = ''
    total = 0
    cheque = []

    money, stocks, market_stocks, offers = update_market_info()

    if purchase.accept.data:
        transactions = list(db_sess.query(Transaction).
                            filter(Transaction.user_id == current_user.id,
                                   Transaction.session_id == get_session_id()))
        company_id = db_sess.query(Offer.company_id).filter(
            Offer.id == transactions[0].offer_id,
            Offer.session_id == get_session_id()
        ).first()[0]
        first_cost = 0
        all_transactions_stocks = 0
        all_sellers_ids = []
        for t in transactions:
            t: Transaction
            offer = db_sess.query(Offer).get(t.offer_id)
            seller_id = offer.user_id

            first_cost += t.stocks * t.price
            if seller_id not in all_sellers_ids:
                all_transactions_stocks += sum(
                    map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                        Stock.user_id == seller_id,
                        Stock.company_id == company_id,
                        Stock.session_id == get_session_id()
                    ))) + \
                                           sum(map(lambda x: x[0],
                                                   db_sess.query(Offer.stocks).filter(
                                                       Offer.user_id == seller_id,
                                                       Offer.company_id == company_id,
                                                       Offer.session_id == get_session_id()
                                                   )))
                all_sellers_ids.append(seller_id)
        all_transactions_stocks += sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
            Stock.user_id == current_user.id,
            Stock.company_id == company_id,
            Stock.session_id == get_session_id()
        ))) + \
            sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
                Offer.user_id == current_user.id,
                Offer.company_id == company_id,
                Offer.session_id == get_session_id()
            )))
        stocks_count = sum(map(lambda x: x[0], list(db_sess.query(Stock.stocks).filter(
            Stock.company_id == company_id,
            Stock.session_id == get_session_id()
        )))) + \
            sum(map(lambda x: x[0], list(db_sess.query(Offer.stocks).filter(
                Offer.company_id == company_id,
                Offer.session_id == get_session_id()
            ))))
        fee = first_cost * (stocks_count - all_transactions_stocks) * get_constant('PROFIT_PERCENT')
        final_cost = first_cost + fee

        customer_wallet = db_sess.query(Wallet).filter(Wallet.user_id == current_user.id).first()
        if customer_wallet.money >= final_cost:
            customer_stock = db_sess.query(Stock). \
                filter(Stock.user_id == current_user.id,
                       Stock.company_id == company_id,
                       Stock.session_id == get_session_id()
                       ).first()

            customer_wallet.money -= final_cost
            db_sess.merge(customer_wallet)

            for t in transactions:
                offer = db_sess.query(Offer).get(t.offer_id)
                if offer.stocks > t.stocks:
                    offer.stocks -= t.stocks
                    offer.reserved_stocks -= t.stocks
                    db_sess.merge(offer)
                elif offer.stocks == t.stocks:
                    db_sess.delete(offer)
                if customer_stock:
                    customer_stock.stocks += t.stocks
                    db_sess.merge(customer_stock)
                else:
                    customer_stock = Stock(
                        session_id=get_session_id(),
                        user_id=current_user.id,
                        company_id=offer.company_id,
                        stocks=t.stocks
                    )
                    db_sess.add(customer_stock)
                db_sess.commit()

                seller_wallet = db_sess.query(Wallet).filter(
                    Wallet.user_id == offer.user_id,
                    Wallet.session_id == get_session_id()
                ).first()
                seller_wallet.money += t.stocks * t.price
                db_sess.merge(seller_wallet)
                db_sess.delete(t)
                db_sess.commit()

            stockholders_ids = set(map(lambda x: x[0], db_sess.query(Stock.user_id).filter(
                Stock.company_id == company_id,
                Stock.session_id == get_session_id()
            ))).union(
                set(map(lambda x: x[0], db_sess.query(Offer.user_id).filter(
                    Offer.company_id == company_id,
                    Offer.session_id == get_session_id()
                )))
            )

            for i in stockholders_ids:
                if i not in all_sellers_ids and i != current_user.id:
                    stockholder_stocks = sum(
                        list(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                            Stock.user_id == i,
                            Stock.session_id == get_session_id()
                        ))) +
                        list(map(lambda x: x[0],
                                 db_sess.query(Offer.stocks).filter(
                                     Offer.user_id == i,
                                     Offer.session_id == get_session_id()
                                 )))
                    )
                    wallet = db_sess.query(Wallet).filter(
                        Wallet.user_id == i,
                        Wallet.session_id == get_session_id()
                    ).first()
                    fee_percent = get_constant('PROFIT_PERCENT')
                    wallet.money += first_cost * fee_percent * stockholder_stocks
                    db_sess.merge(wallet)
                    db_sess.commit()

        else:
            for t in transactions:
                offer = db_sess.query(Offer).get(t.offer_id)
                offer.reserved_stocks -= t.stocks
                db_sess.merge(offer)
                db_sess.delete(t)
            db_sess.commit()
            message = 'На балансе недостаточно средств'

    elif purchase.decline.data:
        transactions = list(db_sess.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.session_id == get_session_id()
        ))
        for t in transactions:
            offer = db_sess.query(Offer).get(t.offer_id).first()
            offer.reserved_stocks -= t.stocks
            db_sess.delete(t)
            db_sess.commit()

    purchase = None
    if form.validate_on_submit() or (form.is_submitted() and form.action.data == 'Инвестировать'):
        if form.action.data == 'Инвестировать':
            if form.amount.data:
                investor_wallet = db_sess.query(Wallet).filter(
                    Wallet.user_id == current_user.id,
                    Wallet.session_id == get_session_id()
                ).first()
                if investor_wallet.money >= form.amount.data:
                    surname, name = form.user.data.split()
                    user_id = db_sess.query(User.id).filter(User.surname == surname,
                                                            User.name == name)
                    wallet = db_sess.query(Wallet).filter(
                        Wallet.user_id == user_id,
                        Wallet.session_id == get_session_id()
                    ).first()
                    wallet.money += form.amount.data
                    investor_wallet.money -= form.amount.data
                    db_sess.merge(investor_wallet)
                    db_sess.merge(wallet)
                    db_sess.commit()
                    message = 'Инвестиция прошла успешно'
                else:
                    message = 'На балансе недостаточно средств'
        elif not form.stocks.data:
            pass
        elif form.action.data == 'Продать':
            company_id = get_company_id(form.company.data)
            company_stocks = list(filter(lambda x: x[0] == form.company.data, stocks))
            if company_stocks:
                company_stocks = company_stocks[0]
                if company_stocks[1] >= form.stocks.data:
                    if form.price.data >= 1:

                        offer = db_sess.query(Offer).filter(
                            Offer.user_id == current_user.id,
                            Offer.company_id == company_id,
                            Offer.price == form.price.data,
                            Offer.session_id == get_session_id()
                        ).first()
                        if not offer:
                            offer = Offer(
                                session_id=get_session_id(),
                                user_id=current_user.id,
                                company_id=company_id,
                                stocks=form.stocks.data,
                                price=form.price.data
                            )
                            db_sess.add(offer)
                        else:
                            offer.stocks += form.stocks.data
                            db_sess.merge(offer)

                        stock = db_sess.query(Stock). \
                            filter(Stock.user_id == current_user.id,
                                   Stock.company_id == company_id,
                                   Stock.session_id == get_session_id()).first()
                        if company_stocks[1] > form.stocks.data:
                            stock.stocks -= form.stocks.data
                            db_sess.merge(stock)
                        else:
                            db_sess.delete(stock)

                        db_sess.commit()

                        message = 'Акции выставлены на продажу'

                    else:
                        message = 'Неверная цена'
                else:
                    message = 'У Вас не хватает акций'
            else:
                message = 'У Вас нет акций этого проекта'
        elif form.action.data == 'Отменить продажу':
            company_id = get_company_id(form.company.data)
            market_company_stocks = list(filter(lambda x: x[0] == form.company.data,
                                                market_stocks))
            if market_company_stocks:
                market_company_stocks = list(filter(lambda x: x[3] == form.price.data,
                                                    market_company_stocks))
                if market_company_stocks:
                    market_company_stocks = market_company_stocks[0]
                    if market_company_stocks[1] - market_company_stocks[2] >= form.stocks.data:
                        user_offer = db_sess.query(Offer). \
                            filter(Offer.user_id == current_user.id,
                                   Offer.price == form.price.data,
                                   Offer.session_id == get_session_id()).first()
                        user_stocks = db_sess.query(Stock). \
                            filter(Stock.user_id == current_user.id,
                                   Stock.company_id == company_id,
                                   Stock.session_id == get_session_id()).first()
                        if not user_stocks:
                            user_stocks = Stock(
                                session_id=get_session_id(),
                                user_id=current_user.id,
                                company_id=company_id,
                                stocks=form.stocks.data
                            )
                            db_sess.add(user_stocks)
                        else:
                            user_stocks.stocks += form.stocks.data
                            db_sess.merge(user_stocks)

                        if market_company_stocks[1] > form.stocks.data or market_company_stocks[2]:
                            user_offer.stocks -= form.stocks.data
                            db_sess.merge(user_offer)
                        else:
                            db_sess.delete(user_offer)
                        db_sess.commit()

                        message = 'Акции сняты с торговой площадки'

                    else:
                        message = 'У Вас не хватает акций на торговой площадке. Также Вы не ' \
                                  'можете снять с продажи уже зарезервированные акции '
                else:
                    message = 'На торговой площадке нет Ваших акций данного проекта с указанной ' \
                              'ценой '
            else:
                message = 'На торговой площадке нет Ваших акций указанного проекта'
        elif form.action.data == 'Купить':
            market_offers = list(map(lambda x: (get_company_title(x[0]), x[1], x[2], x[3], x[4]),
                                     db_sess.query(Offer.company_id,
                                                   Offer.stocks,
                                                   Offer.reserved_stocks,
                                                   Offer.price,
                                                   Offer.user_id).
                                     filter(Offer.company_id == get_company_id(form.company.data),
                                            Offer.user_id != current_user.id,
                                            Offer.session_id == get_session_id()
                                            )))
            if market_offers:
                if sum(map(lambda x: x[1] - x[2], market_offers)) >= form.stocks.data:
                    purchase = PurchaseForm()
                    stocks_need = form.stocks.data
                    cheque = []
                    market_offers.sort(key=lambda x: x[3])
                    transaction_users = []
                    while stocks_need:
                        available_stocks = market_offers[0][1] - market_offers[0][2]
                        if available_stocks and available_stocks <= stocks_need:
                            transaction_users.append(market_offers[0][4])
                            stocks_need -= available_stocks
                            offer = db_sess.query(Offer). \
                                filter(Offer.company_id == get_company_id(market_offers[0][0]),
                                       Offer.stocks == market_offers[0][1],
                                       Offer.reserved_stocks == market_offers[0][2],
                                       Offer.price == market_offers[0][3],
                                       Offer.session_id == get_session_id()
                                       ).first()
                            transaction = Transaction(
                                session_id=get_session_id(),
                                user_id=current_user.id,
                                offer_id=offer.id,
                                stocks=available_stocks,
                                price=offer.price
                            )
                            db_sess.add(transaction)
                            if not offer:
                                message = 'На торговой площадке нет в наличии такого ' \
                                          'количества акций указанного проекта'
                            else:
                                offer.reserved_stocks += available_stocks
                                cheque.append((get_company_title(offer.company_id),
                                               available_stocks,
                                               offer.price,
                                               available_stocks * offer.price))
                                db_sess.merge(offer)
                                db_sess.commit()
                        elif available_stocks and available_stocks > stocks_need:
                            transaction_users.append(market_offers[0][4])
                            offer = db_sess.query(Offer). \
                                filter(Offer.company_id == get_company_id(market_offers[0][0]),
                                       Offer.stocks == market_offers[0][1],
                                       Offer.reserved_stocks == market_offers[0][2],
                                       Offer.price == market_offers[0][3],
                                       Offer.session_id == get_session_id()
                                       ).first()
                            transaction = Transaction(
                                session_id=get_session_id(),
                                user_id=current_user.id,
                                offer_id=offer.id,
                                stocks=stocks_need,
                                price=offer.price
                            )
                            db_sess.add(transaction)
                            if not offer:
                                message = 'На торговой площадке нет в наличии такого ' \
                                          'количества акций указанного проекта'
                            else:
                                offer.reserved_stocks += stocks_need
                                cheque.append((get_company_title(offer.company_id),
                                               stocks_need,
                                               offer.price,
                                               stocks_need * offer.price))

                                stocks_need = 0
                                db_sess.merge(offer)
                                db_sess.commit()
                        market_offers.pop(0)
                    total = sum(map(lambda x: x[-1], cheque))
                    all_project_stocks = sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                        Stock.company_id == get_company_id(form.company.data),
                        Stock.session_id == get_session_id()
                    ))) + \
                        sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
                            Offer.company_id == get_company_id(form.company.data),
                            Offer.session_id == get_session_id()
                        )))

                    transaction_stocks = 0
                    company_id = get_company_id(form.company.data)
                    for user_id in set(transaction_users):
                        transaction_stocks += sum(map(lambda x: x[0], db_sess.query(Stock.stocks).
                                                      filter(
                            Stock.company_id == company_id,
                            Stock.user_id == user_id,
                            Stock.session_id == get_session_id()
                        ))) + \
                                              sum(map(lambda x: x[0],
                                                      db_sess.query(Offer.stocks).filter(
                                                          Offer.company_id == company_id,
                                                          Offer.user_id == user_id,
                                                          Offer.session_id == get_session_id()
                                                      )))

                    fee = (all_project_stocks - transaction_stocks) * total * 0.001
                    total += fee
                    cheque.append(('Комиссия', '-', '-', fee))

                else:
                    message = 'На торговой площадке нет в наличии такого количества акций ' \
                              'указанного проекта '
            else:
                message = 'На торговой площадке нет акций указанного проекта'

    money, stocks, market_stocks, offers = update_market_info()

    market_stocks = sorted(market_stocks, key=lambda x: x[-1])
    offers = sorted(offers, key=lambda x: x[-1])

    return render_template(template,
                           game_role=get_game_roles(),
                           form=form,
                           title='Торговая площадка',
                           message=message,
                           money=money,
                           stocks=stocks,
                           market_stocks=market_stocks,
                           offers=offers,
                           purchase=purchase,
                           cheque=cheque,
                           total=total)
