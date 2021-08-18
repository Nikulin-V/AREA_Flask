#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required

from data.functions import get_game_roles, get_constant
from market import market
from tools.tools import game_running_required


@market.route('/create-company', methods=['GET', 'POST'])
@login_required
@game_running_required
def create_company():
    if not get_game_roles():
        abort(404)

    return render_template("market/create_company.html",
                           title='Открыть компанию',
                           new_company_fee=float(get_constant('NEW_COMPANY_FEE')))
