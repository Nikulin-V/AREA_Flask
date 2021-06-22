#  Nikulin Vasily (c) 2021
from flask_login import current_user

from data import db_session
from data.companies import Company
from data.offers import Offer
from data.stocks import Stock
from data.votes import Vote
from data.users import User
from data.wallets import Wallet


def get_company_title(identifier):
    return db_session.create_session().query(Company.title). \
        filter(Company.id == identifier).first()[0]


def get_company_id(title):
    return db_session.create_session().query(Company.id). \
        filter(Company.title == title).first()[0]


def update_market_info():
    db_sess = db_session.create_session()
    # Получаем акции пользователя
    # title | stocks
    stocks = list(map(lambda x: (get_company_title(x[0]), x[1]),
                      db_sess.query(Stock.company_id, Stock.stocks).
                      filter(Stock.user_id == current_user.id)))

    # Получаем акции пользователя на торговой площадке
    # title | stocks | reserved_stocks | price
    market_stocks = list(map(lambda x: (get_company_title(x[0]), x[1], x[2], x[3]),
                             db_sess.query(Offer.company_id, Offer.stocks,
                                           Offer.reserved_stocks, Offer.price).
                             filter(Offer.user_id == current_user.id)))

    # Получаем текущие предложения на рынке
    # title | stocks | reserved_stocks | price
    offers = list(map(lambda x: (get_company_title(x[0]), x[1], x[2], x[3]),
                      db_sess.query(Offer.company_id, Offer.stocks,
                                    Offer.reserved_stocks, Offer.price)))

    # Получаем баланс кошелька
    money = db_sess.query(Wallet.money).filter(Wallet.user_id == current_user.id).first()
    if not money:
        default = 1000
        if 'Эксперт' in current_user.role:
            default = 10000
        wallet = Wallet(
            user_id=current_user.id,
            money=default
        )
        db_sess.add(wallet)
        db_sess.commit()
        money = default
    else:
        money = round(money[0], 2)
        if money == int(money):
            money = int(money)

    return money, stocks, market_stocks, offers


def evaluate_form(form):
    db_sess = db_session.create_session()
    companies = dict()
    sections = sorted(list(map(lambda x: x[0], set(list(db_sess.query(Company.section))))))

    # row structure: id | title | points | form
    for section in sections:
        data = list(db_sess.query(Company.id, Company.title).filter(Company.section == section))
        for row_id in range(len(data)):
            points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                  filter(Vote.company_id == data[row_id][0]))))
            data[row_id] = list(data[row_id])
            data[row_id] += [points]
        companies[section] = sorted(data, key=lambda x: -x[2])

    form.section.choices = sorted(list(set(map(lambda x: x[0],
                                               list(db_sess.query(Company.section))))))

    if not form.section.data or form.section.data not in form.section.choices:
        form.section.errors = []
        form.section.data = form.section.choices[0]
    form.company.choices = sorted(list(map(lambda x: x[0],
                                           list(db_sess.query(Company.title).
                                                filter(Company.section == form.section.data)))))

    users = list(map(lambda x: ' '.join(list(db_sess.query(User.surname, User.name).
                                             filter(User.id == x[0]).first())),
                     db_sess.query(Wallet.user_id)))

    if form.user:
        form.user.choices = users
        if not form.user.data:
            form.user.data = users[0]

    return sections, companies
