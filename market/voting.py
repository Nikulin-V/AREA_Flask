#  Nikulin Vasily © 2021
from flask import render_template
from flask_babel import _
from flask_login import login_required

from market import market
from tools.tools import game_running_required


@market.route('/companies-management')
@login_required
@game_running_required
def stockholders_voting():
    return render_template("market/companies_management.html",
                           title=_('Управление компаниями'))
