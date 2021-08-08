#  Nikulin Vasily © 2021

import flask
from flask import request, jsonify
from flask_login import current_user
from flask_socketio import emit

from config import HOST, DEV_HOST
from data import db_session
from data.functions import get_session_id
from data.offers import Offer
from data.stocks import Stock


def use_subdomains(subdomains=None):
    if subdomains is None:
        subdomains = ['area']

    def subdomains_decorator(func):

        def wrapper(*args, **kwargs):
            subdomain = get_subdomain()
            if subdomain in subdomains:
                return func(*args, **kwargs)
            else:
                return 'Неверный поддомен сайта'

        return wrapper

    return subdomains_decorator


def get_subdomain():
    host = request.host
    if host == HOST or host == DEV_HOST:
        return 'area'
    elif host.endswith(HOST) or host.split(':')[0].endswith(HOST) or \
            host.endswith(DEV_HOST) or host.split(':')[0].endswith(DEV_HOST):
        return host.split('.')[0]


def get_object_data_from_request(object_data: dict, keys: list, ):
    if object_data is None:
        object_data = {}

    for key in keys:
        if key not in object_data.keys():
            object_data[key] = request.args.get(key)

    return object_data


def is_stockholder(company_id):
    db_sess = db_session.create_session()
    stocks = db_sess.query(Stock).filter(
        Stock.session_id == get_session_id(),
        Stock.company_id == company_id,
        Stock.user_id == current_user.id).all()
    offers = db_sess.query(Offer).filter(
        Offer.session_id == get_session_id(),
        Offer.company_id == company_id,
        Offer.user_id == current_user.id).all()
    if stocks or offers:
        return True
    return False


def votes(stockholders, company_id):
    if stockholders:
        stockholders = list(int(s_id) for s_id in str(stockholders).split(';') if s_id)
    else:
        stockholders = []

    db_sess = db_session.create_session()

    all_stockholders = len(set(db_sess.query(Stock.user_id).filter(Stock.company_id == company_id)))
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


def send_response(event_name, response=None):
    if hasattr(flask.request, 'namespace'):
        if response is None:
            emit(event_name)
        else:
            emit(event_name, response)
    else:
        return jsonify(response)