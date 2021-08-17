#  Nikulin Vasily © 2021
import datetime

from flask_login import login_required, current_user

from area.api import clients_sid
from config import icons
from data import db_session
from data.db_functions import get_session_id
from data.functions import get_constant
from data.sessions import Session
from data.users import User
from data.wallets import Wallet
from market.api import api, socket
from tools.tools import send_response, fillJson
from tools.url import url


@socket.on('getWalletMoney')
@api.route('/api/wallet', methods=['GET'])
@login_required
def getWalletMoney():
    event_name = 'getWalletMoney'

    db_sess = db_session.create_session()

    wallet = db_sess.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    wallet = check_wallet(wallet, db_sess)

    response = {
        'message': 'Success',
        'money': wallet.money
    }

    return send_response(event_name, response)


@socket.on('getWallets')
@api.route('/api/wallets', methods=['GET'])
def getWallets():
    event_name = 'getWallets'

    db_sess = db_session.create_session()

    players_ids = db_sess.query(Session).get(get_session_id()).players_ids.split(';')
    wallets = dict()
    for player_id in players_ids:
        if player_id == current_user.id:
            continue
        user = db_sess.query(User).get(player_id)
        wallet = db_sess.query(Wallet.id).filter(Wallet.user_id == player_id).first()
        wallet = check_wallet(wallet, db_sess, player_id)
        wallets[f'{user.surname} {user.name}'] = wallet.id
        wallets = dict(sorted(list(wallets.items()), key=lambda x: x[0]))
    return send_response(
        event_name,
        {
            'message': 'Success',
            'wallets': wallets,
            'errors': []
        }
    )


@socket.on('investWallet')
@api.route('/api/wallets', methods=['PATCH'])
@login_required
def investWallet(json=None):
    if json is None:
        json = dict()

    fillJson(json, ['walletId', 'money'])

    event_name = 'investWallet'

    recipient_wallet_id = json['walletId']
    money = json['money']

    if not recipient_wallet_id:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify recipient wallet id']
            }
        )

    if money is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify money']
            }
        )

    try:
        money = float(money)
        if money <= 0:
            raise ValueError
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Money must be real number']
            }
        )

    db_sess = db_session.create_session()

    recipient_wallet = db_sess.query(Wallet).get(recipient_wallet_id)
    if not recipient_wallet:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Wallet not found']
            }
        )

    investor_wallet = db_sess.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    investor_wallet = check_wallet(investor_wallet, db_sess)

    if investor_wallet.money < money:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Not enough money']
            }
        )

    investor_wallet.money -= money
    recipient_wallet.money += money

    db_sess.merge(investor_wallet)
    db_sess.merge(recipient_wallet)

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
                    'logoSource': icons['investment'],
                    'company': f'Инвестиция: {money}'
                               f'<span class="material-icons-round md-money">paid</span>',
                    'author': f'{current_user.surname} {current_user.name}',
                    'date': datetime.datetime.now().strftime('%d %B'),
                    'time': datetime.datetime.now().strftime('%H:%M'),
                    'redirectLink': url("market.marketplace")
                }
            ],
            'errors': []
        },
        room=clients_sid[recipient_wallet.user_id]
    )


def check_wallet(wallet, db_sess, user_id=None):
    if user_id is None:
        user_id = current_user.id
    if wallet is None:
        wallet = Wallet(
            session_id=get_session_id(),
            user_id=user_id,
            money=get_constant('START_WALLET_MONEY')
        )
        db_sess.add(wallet)
        db_sess.commit()
    return wallet
