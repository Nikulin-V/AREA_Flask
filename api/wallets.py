#  Nikulin Vasily © 2021
from flask_login import login_required, current_user

from api import api, sock
from data import db_session
from data.db_functions import get_session_id
from data.functions import get_constant
from data.wallets import Wallet
from tools.tools import send_response


@sock.on('getWalletMoney')
@api.route('/api/wallets', methods=['GET'])
@login_required
def getWallet():
    event_name = 'getWalletMoney'

    db_sess = db_session.create_session()
    wallet = db_sess.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if wallet is None:
        wallet = Wallet(
            session_id=get_session_id(),
            user_id=current_user.id,
            money=get_constant('START_WALLET_MONEY')
        )
        db_sess.add(wallet)
        db_sess.commit()

    response = {
        'message': 'Success',
        'money': wallet.money
    }

    return send_response(event_name, response)
