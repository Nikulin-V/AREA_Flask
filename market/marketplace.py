#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required

from data.functions import get_game_roles
from market import market
from tools.tools import game_running_required


@market.route('/marketplace', methods=['GET', 'POST'])
@login_required
@game_running_required
def marketplace():
    if not get_game_roles():
        abort(404)

    return render_template("market/marketplace.html",
                           title='Торговая площадка')
