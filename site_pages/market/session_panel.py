#  Nikulin Vasily (c) 2021

#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.config import Constant
from data.functions import get_game_roles, get_session_id, get_constant
from forms.config_management import ConfigManagementForm
from tools import use_subdomains

game_panel_page = Blueprint('game-panel', __name__)
app = game_panel_page


@app.route('/game-panel', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}session-panel.html')
@login_required
def game_panel(template, subdomain='market'):
    if 'Admin' not in get_game_roles():
        abort(404)

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

    if not form.game_run.data:
        form.game_run.data = get_constant('GAME_RUN')

    if not form.start_wallet_money.data:
        form.start_wallet_money.data = get_constant('START_WALLET_MONEY')

    if not form.fee.data:
        form.fee.data = get_constant('FEE_FOR_STOCK')

    if not form.new_company_fee.data:
        form.new_company_fee.data = get_constant('NEW_COMPANY_FEE')

    if not form.start_stocks.data:
        form.start_stocks.data = get_constant('START_STOCKS')

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Управление фондовой биржей',
                           message=message,
                           form=form)
