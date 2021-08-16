#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required

from market import market
from tools.tools import game_running_required


@market.route('/companies', methods=['GET', 'POST'])
@login_required
@game_running_required
def companies():
    return render_template("market/companies.html",
                           title='Компании')
