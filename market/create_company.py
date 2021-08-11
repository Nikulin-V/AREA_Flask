#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles, get_constant
from market import market
from tools.tools import game_running_required


@market.route('/create-company', methods=['GET', 'POST'])
@mobile_template('market/{mobile/}create-company.html')
@login_required
@game_running_required
def create_company(template):
    if not get_game_roles():
        abort(404)

    return render_template(template,
                           title='Открыть компанию',
                           new_company_fee=get_constant('NEW_COMPANY_FEE'))
