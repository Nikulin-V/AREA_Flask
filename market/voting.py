#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required

from market import market
from tools.tools import game_running_required, roles_required


@market.route('/companies-management')
@roles_required('user', 'player')
@login_required
@game_running_required
def stockholders_voting():
    return render_template("market/companies_management.html",
                           title='Управление компаниями')
