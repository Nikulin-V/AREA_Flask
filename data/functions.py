#  Nikulin Vasily © 2021
from flask_login import current_user, AnonymousUserMixin
from sqlalchemy import or_

from data import db_session
from data.companies import Company
from data.config import Constant
from data.db_functions import get_session_id
from data.offers import Offer
from data.sessions import Session
from data.stocks import Stock
from data.users import User
from data.votes import Vote
from data.wallets import Wallet


def get_constant(name):
    db_session.global_init('db/database.sqlite')
    db_sess = db_session.create_session()
    constant = db_sess.query(Constant.value). \
        filter(Constant.name == name,
               Constant.session_id == get_session_id()).first()
    if constant:
        constant = constant[0]
    if int(constant) == float(constant):
        return int(constant)
    return float(constant)


def get_company_title(identifier):
    res = db_session.create_session().query(Company.title). \
        filter(Company.id == identifier,
               Company.session_id == get_session_id()).first()
    if res is not None:
        return res[0]


def get_company_id(title):
    res = db_session.create_session().query(Company.id). \
        filter(Company.title == title,
               Company.session_id == get_session_id()).first()
    if res is not None:
        return res[0]


def update_market_info():
    db_sess = db_session.create_session()
    # Получаем акции пользователя
    # title | stocks
    stocks = list(map(lambda x: (get_company_title(x[0]), x[1]),
                      db_sess.query(Stock.company_id, Stock.stocks).
                      filter(
                          Stock.user_id == current_user.id,
                          Stock.session_id == get_session_id()
                      )))

    # Получаем акции пользователя на торговой площадке
    # title | stocks | reserved_stocks | price
    market_stocks = list(map(lambda x: (get_company_title(x[0]), x[1], x[2], x[3]),
                             db_sess.query(Offer.company_id, Offer.stocks,
                                           Offer.reserved_stocks, Offer.price).
                             filter(
                                 Offer.user_id == current_user.id,
                                 Offer.session_id == get_session_id()
                             )))

    # Получаем текущие предложения на рынке
    # title | stocks | reserved_stocks | price
    offers = list(map(lambda x: (get_company_title(x[0]), x[1], x[2], x[3]),
                      db_sess.query(Offer.company_id, Offer.stocks,
                                    Offer.reserved_stocks, Offer.price).
                      filter(
                          Offer.session_id == get_session_id()
                      )))

    # Получаем баланс кошелька
    money = db_sess.query(Wallet.money).filter(
        Wallet.user_id == current_user.id,
        Wallet.session_id == get_session_id()
    ).first()
    if not money:
        wallet = Wallet(
            session_id=get_session_id(),
            user_id=current_user.id,
            money=get_constant('START_WALLET_MONEY')
        )
        db_sess.add(wallet)
        db_sess.commit()
    else:
        money = round(money[0], 2)
        if money == int(money):
            money = int(money)

    return money, stocks, market_stocks, offers


def evaluate_form(form):
    db_sess = db_session.create_session()
    companies = dict()
    sectors = sorted(list(map(lambda x: x[0], set(list(db_sess.query(Company.sector).filter(
        Company.session_id == get_session_id()
    ))))))

    # row structure: id | title | points | form
    for sector in sectors:
        data = list(db_sess.query(Company.id, Company.title).filter(
            Company.sector == sector,
            Company.session_id == get_session_id()
        ))
        for row_id in range(len(data)):
            points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).filter(
                Vote.company_id == data[row_id][0],
                Vote.session_id == get_session_id()
            ))))
            data[row_id] = list(data[row_id])
            data[row_id] += [points]
        companies[sector] = sorted(data, key=lambda x: -x[2])

    form.sector.choices = sorted(list(set(map(lambda x: x[0],
                                              list(db_sess.query(Company.sector).filter(
                                                  Company.session_id == get_session_id()
                                              ))))))

    if not form.sector.data or form.sector.data not in form.sector.choices:
        form.sector.errors = []
        if form.sector.choices:
            form.sector.data = form.sector.choices[0]
    form.company.choices = sorted(list(map(lambda x: x[0],
                                           list(db_sess.query(Company.title).
                                                filter(Company.sector == form.sector.data,
                                                       Company.session_id == get_session_id())))))

    users = list(map(lambda x: ' '.join(list(db_sess.query(User.surname, User.name).
                                             filter(User.id == x[0]).first())),
                     db_sess.query(Wallet.user_id)))

    if form.user:
        form.user.choices = users
        if not form.user.data and users:
            form.user.data = users[0]

    return sectors, companies


def get_game_roles(new_session_id=None):
    roles = []
    if not isinstance(current_user, AnonymousUserMixin):
        db_sess = db_session.create_session()

        identifier = str(current_user.id)
        session_id = current_user.game_session_id
        session = db_sess.query(Session).filter(Session.id == session_id).first()
        if not session and new_session_id:
            session = db_sess.query(Session).get(new_session_id)
        if session:
            if identifier in str(session.admins_ids).split(';'):
                roles.append('Admin')
            if identifier in str(session.players_ids).split(';'):
                roles.append('Player')

    return roles


def get_game_sessions():
    db_sess = db_session.create_session()

    identifier = str(current_user.id)

    data = db_sess.query(Session).filter(or_(Session.admins_ids.contains(str(identifier)),
                                             Session.players_ids.contains(str(identifier)))).all()

    sessions = []
    for session_id in range(len(data)):
        if identifier in str(data[session_id].admins_ids) or \
                identifier in str(data[session_id].players_ids):
            sessions.append(data[session_id])

    sessions.sort(key=lambda x: x.title)

    return sessions
