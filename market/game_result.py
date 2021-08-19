#  Nikulin Vasily © 2021
from flask import render_template, abort, redirect
from flask_login import login_required

from data import db_session
from data.functions import get_constant, get_game_roles, get_session_id
from data.users import User
from data.wallets import Wallet
from market import market


@market.route('/game-result')
@login_required
def game_result():
    if get_constant('GAME_RUN'):
        return redirect('/marketplace')

    if not get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    data = list(db_sess.query(Wallet.user_id, Wallet.money).filter(
        Wallet.session_id == get_session_id()
    ).all())
    data.sort(key=lambda x: -x[1])
    players_wallets = list()
    i = 1
    for user_id, money in data:
        print(db_sess.query(User.surname, User.name).filter(
            User.id == user_id
        ).first())
        user = ' '.join(db_sess.query(User.surname, User.name).filter(
            User.id == user_id
        ).first())
        players_wallets.append([i, user, round(money)])
        i += 1

    balances = sorted(list(set(map(lambda x: x[2], players_wallets))), reverse=True)
    for balance in balances:
        count_wallets = len(list(db_sess.query(Wallet).
                                 filter(Wallet.money == balance,
                                        Wallet.session_id == get_session_id())))
        if count_wallets > 1:
            current_wallets = list(filter(lambda x: x[2] == balance, players_wallets))
            current_wallets.sort()
            i = f'{current_wallets[0][0]}-{current_wallets[-1][0]}'
            for wallet_id in range(len(players_wallets)):
                if players_wallets[wallet_id][2] == balance:
                    players_wallets[wallet_id][0] = i

    return render_template("market/session_result.html",
                           title='Итоги торгов',
                           wallets=players_wallets)
