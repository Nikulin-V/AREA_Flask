#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.projects_8_class_offers import Offer
from data.projects_8_class_stocks import Stock
from data.projects_8_class_transactions import Transaction
from data.users import User
from data.wallets import Wallet
from forms.purchase import PurchaseForm
from forms.stocks import StocksForm
from site_pages.functions import evaluate_form, update_market_info, get_project_id, \
    get_project_title

projects_marketplace_page = Blueprint('projects-marketplace', __name__)
app = projects_marketplace_page


@app.route('/8-classes-market', methods=['GET', 'POST'])
@mobile_template('{mobile/}8-classes-market.html')
@login_required
def market_8_class(template):
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
                            filter(Transaction.user_id == current_user.id))
        for t in transactions:
            t: Transaction
            offer = db_sess.query(Offer).filter(Offer.id == t.offer_id).first()
            seller_id = offer.user_id
            customer_id = t.user_id

            seller_wallet = db_sess.query(Wallet).filter(Wallet.user_id == seller_id).first()
            customer_wallet = db_sess.query(Wallet).filter(Wallet.user_id == customer_id).first()
            stockholders_ids = list(set(db_sess.query(Stock.user_id, Stock.stocks).
                                        filter(Stock.project_id == offer.project_id,
                                               Stock.user_id != seller_id)))
            first_cost = t.stocks * t.price
            final_cost = first_cost + first_cost * (100 - t.stocks) * 0.001
            if customer_wallet.money >= final_cost:
                customer_stock = db_sess.query(Stock). \
                    filter(Stock.user_id == current_user.id,
                           Stock.project_id == offer.project_id).first()
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
                        user_id=current_user.id,
                        project_id=offer.project_id,
                        stocks=t.stocks
                    )
                    db_sess.add(customer_stock)
                db_sess.commit()
                customer_wallet.money -= final_cost
                seller_wallet.money += first_cost
                db_sess.merge(customer_wallet)
                db_sess.merge(seller_wallet)
                seller_stock = db_sess.query(Stock). \
                    filter(Stock.user_id == seller_id,
                           Stock.project_id == offer.project_id).first()
                if t.stocks < seller_stock.stocks:
                    seller_stock.stocks -= t.stocks
                for user_id, stocks in stockholders_ids:
                    wallet = db_sess.query(Wallet).filter(Wallet.user_id == user_id).first()
                    wallet.money += first_cost * stocks * 0.01
                    db_sess.merge(wallet)
                db_sess.delete(t)
                db_sess.commit()
            else:
                offer = db_sess.query(Offer).filter(Offer.id == t.offer_id).first()
                offer.reserved_stocks -= t.stocks
                db_sess.merge(offer)
                db_sess.delete(t)
                db_sess.commit()
                message = 'На балансе недостаточно средств'

    elif purchase.decline.data:
        transactions = list(db_sess.query(Transaction).
                            filter(Transaction.user_id == current_user.id))
        for t in transactions:
            offer = db_sess.query(Offer).filter(Offer.id == t.offer_id).first()
            offer.reserved_stocks -= t.stocks
            db_sess.delete(t)
            db_sess.commit()

    purchase = None
    if form.validate_on_submit() or (form.is_submitted() and form.action.data == 'Инвестировать'):
        if form.action.data == 'Инвестировать':
            if form.amount.data:
                investor_wallet = db_sess.query(Wallet). \
                    filter(Wallet.user_id == current_user.id).first()
                if investor_wallet.money >= form.amount.data:
                    surname, name = form.user.data.split()
                    user_id = db_sess.query(User.id).filter(User.surname == surname,
                                                            User.name == name)
                    wallet = db_sess.query(Wallet).filter(Wallet.user_id == user_id).first()
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
            project_id = get_project_id(form.project.data)
            project_stocks = list(filter(lambda x: x[0] == form.project.data, stocks))
            if project_stocks:
                project_stocks = project_stocks[0]
                if project_stocks[1] >= form.stocks.data:
                    if form.price.data >= 1:

                        offer = db_sess.query(Offer). \
                            filter(Offer.user_id == current_user.id,
                                   Offer.project_id == project_id,
                                   Offer.price == form.price.data).first()
                        if not offer:
                            offer = Offer(
                                user_id=current_user.id,
                                project_id=project_id,
                                stocks=form.stocks.data,
                                price=form.price.data
                            )
                            db_sess.add(offer)
                        else:
                            offer.stocks += form.stocks.data
                            db_sess.merge(offer)

                        stock = db_sess.query(Stock). \
                            filter(Stock.user_id == current_user.id,
                                   Stock.project_id == project_id).first()
                        if project_stocks[1] > form.stocks.data:
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
            project_id = get_project_id(form.project.data)
            market_project_stocks = list(filter(lambda x: x[0] == form.project.data,
                                                market_stocks))
            if market_project_stocks:
                market_project_stocks = list(filter(lambda x: x[3] == form.price.data,
                                                    market_project_stocks))
                if market_project_stocks:
                    market_project_stocks = market_project_stocks[0]
                    if market_project_stocks[1] - market_project_stocks[2] >= form.stocks.data:
                        user_offer = db_sess.query(Offer). \
                            filter(Offer.user_id == current_user.id,
                                   Offer.price == form.price.data).first()
                        user_stocks = db_sess.query(Stock). \
                            filter(Stock.user_id == current_user.id,
                                   Stock.project_id == project_id).first()
                        if not user_stocks:
                            user_stocks = Stock(
                                user_id=current_user.id,
                                project_id=project_id,
                                stocks=form.stocks.data
                            )
                            db_sess.add(user_stocks)
                        else:
                            user_stocks.stocks += form.stocks.data
                            db_sess.merge(user_stocks)

                        if market_project_stocks[1] > form.stocks.data or market_project_stocks[2]:
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
            market_offers = list(map(lambda x: (get_project_title(x[0]), x[1], x[2], x[3]),
                                     db_sess.query(Offer.project_id,
                                                   Offer.stocks,
                                                   Offer.reserved_stocks,
                                                   Offer.price).
                                     filter(Offer.project_id == get_project_id(form.project.data),
                                            Offer.user_id != current_user.id)))
            if market_offers:
                if sum(map(lambda x: x[1] - x[2], market_offers)) >= form.stocks.data:
                    purchase = PurchaseForm()
                    stocks_need = form.stocks.data
                    cheque = []
                    market_offers.sort(key=lambda x: x[-1])
                    while stocks_need:
                        available_stocks = market_offers[0][1] - market_offers[0][2]
                        if available_stocks and available_stocks <= stocks_need:
                            stocks_need -= available_stocks
                            offer = db_sess.query(Offer). \
                                filter(Offer.project_id == get_project_id(market_offers[0][0]),
                                       Offer.stocks == market_offers[0][1],
                                       Offer.reserved_stocks == market_offers[0][2]).first()
                            transaction = Transaction(
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
                                cheque.append((get_project_title(offer.project_id),
                                               available_stocks,
                                               offer.price,
                                               available_stocks * offer.price))
                                db_sess.merge(offer)
                                db_sess.commit()
                        elif available_stocks and available_stocks > stocks_need:
                            offer = db_sess.query(Offer). \
                                filter(Offer.project_id == get_project_id(market_offers[0][0]),
                                       Offer.stocks == market_offers[0][1],
                                       Offer.reserved_stocks == market_offers[0][2]).first()
                            transaction = Transaction(
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
                                cheque.append((get_project_title(offer.project_id),
                                               stocks_need,
                                               offer.price,
                                               stocks_need * offer.price))

                                stocks_need = 0
                                db_sess.merge(offer)
                                db_sess.commit()
                        market_offers.pop(0)

                    total = sum(map(lambda x: x[-1], cheque))
                    cheque.append(('Комиссия', '-', '-',
                                   (100 - sum(map(lambda x: x[1], cheque))) * total * 0.001))

                else:
                    message = 'На торговой площадке нет в наличии такого количества акций ' \
                              'указанного проекта '
            else:
                message = 'На торговой площадке нет акций указанного проекта'

    money, stocks, market_stocks, offers = update_market_info()

    market_stocks = sorted(market_stocks, key=lambda x: x[-1])
    offers = sorted(offers, key=lambda x: x[-1])

    return render_template(template,
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
