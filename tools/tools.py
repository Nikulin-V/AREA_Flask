#  Nikulin Vasily © 2021
import functools
import os

import flask
from flask import request, jsonify, redirect, abort
from flask_login import current_user, AnonymousUserMixin
from flask_socketio import emit

from data import db_session
from data.functions import get_session_id, get_constant
from data.offers import Offer
from data.stocks import Stock
from data.wallets import Wallet


def is_stockholder(company_id, user_id=None, session_id=None):
    if user_id is None:
        user_id = current_user.id
    if session_id is None:
        session_id = current_user.game_session_id
    db_sess = db_session.create_session()

    stocks = db_sess.query(Stock).filter(
        Stock.session_id == session_id,
        Stock.company_id == company_id,
        Stock.user_id == user_id).all()
    offers = db_sess.query(Offer).filter(
        Offer.session_id == session_id,
        Offer.company_id == company_id,
        Offer.user_id == user_id).all()
    if stocks or offers:
        return True
    return False


def votes(stockholders, company_id):
    if stockholders:
        stockholders = list(str(s_id) for s_id in str(stockholders).split(';') if s_id)
    else:
        stockholders = []

    db_sess = db_session.create_session()

    all_stockholders = len(set(list(db_sess.query(Stock.user_id).filter(
        Stock.company_id == company_id
    )) + list(db_sess.query(Offer.user_id).filter(Offer.company_id == company_id))))
    voted_for_stockholders = len(stockholders)

    return voted_for_stockholders, all_stockholders


def is_voted(stockholders):
    if str(current_user.id) in str(stockholders).split(';'):
        return True
    return False


def fillJson(json, args):
    for arg in args:
        if arg not in json.keys():
            json[arg] = request.args.get(arg)


def send_response(event_name, response=None, *args, **kwargs):
    if hasattr(flask.request, 'namespace'):
        if response is None:
            emit(event_name, *args, **kwargs)
        else:
            emit(event_name, response, *args, **kwargs)
    else:
        return jsonify(response)


def deposit_wallet(user_id, money):
    db_sess = db_session.create_session()
    wallet = db_sess.query(Wallet).filter(Wallet.user_id == user_id).first()
    if wallet is None:
        wallet = Wallet(
            session_id=get_session_id(),
            user_id=user_id,
            money=float(get_constant('START_WALLET_MONEY'))
        )
        db_sess.add(wallet)
    wallet.money += money
    db_sess.commit()


def safe_remove(file):
    if os.path.exists(file):
        os.remove(file)
        return True
    return False


def game_running_required(func):
    @functools.wraps(func)
    def game_running_wrapper(*args, **kwargs):
        if get_constant('GAME_RUN'):
            return func(*args, **kwargs)
        return redirect('/game-result')

    return game_running_wrapper


def roles_required(*roles):
    def decorator(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            if isinstance(current_user, AnonymousUserMixin):
                return abort(401)
            if all([current_user.has_role(role)] for role in roles):
                return func(*args, **kwargs)
            return abort(403)

        return decorated_view

    return decorator


def roles_allowed(*roles):
    def decorator(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            if isinstance(current_user, AnonymousUserMixin):
                return abort(401)
            if any([current_user.has_role(role)] for role in roles):
                return func(*args, **kwargs)
            return abort(403)

        return decorated_view

    return decorator
