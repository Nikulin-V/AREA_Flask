#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required

from data import db_session
from data.config import Constant
from data.functions import get_game_roles, get_session_id, get_constant
from forms.config_management import ConfigManagementForm
from market import market


@market.route('/game-panel', methods=['GET', 'POST'])
@login_required
def game_panel():
    if 'Admin' not in get_game_roles():
        abort(403)

    db_sess = db_session.create_session()

    form = ConfigManagementForm()
    message = ''

    if form.validate_on_submit():
        game_run = db_sess.query(Constant).filter(Constant.name == 'GAME_RUN',
                                                  Constant.session_id == get_session_id()).first()
        game_run.value = 1 if form.game_run.data else 0
        db_sess.merge(game_run)

        constants = [
            ('GAME_RUN', form.game_run.data),
            ('START_WALLET_MONEY', form.start_wallet_money.data),
            ('FEE_FOR_STOCK', form.fee.data),
            ('NEW_COMPANY_FEE', form.new_company_fee.data),
            ('START_STOCKS', form.start_stocks.data)
        ]

        for constant_name, form_field_data in constants[1:]:
            if form_field_data:
                constant = db_sess.query(Constant).filter(
                    Constant.name == constant_name,
                    Constant.session_id == get_session_id()).first()
                constant.value = form_field_data
                db_sess.merge(constant)

        db_sess.commit()
        message = 'Сохранено'

    form.game_run.data = get_constant('GAME_RUN')

    if not form.start_wallet_money.data:
        form.start_wallet_money.data = get_constant('START_WALLET_MONEY')

    if not form.fee.data:
        form.fee.data = get_constant('FEE_FOR_STOCK')

    if not form.new_company_fee.data:
        form.new_company_fee.data = get_constant('NEW_COMPANY_FEE')

    if not form.start_stocks.data:
        form.start_stocks.data = get_constant('START_STOCKS')

    return render_template("market/session_panel.html",
                           title='Управление фондовой биржей',
                           message=message,
                           form=form)
