#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required

from data.functions import get_game_roles
from market import market
from tools.tools import roles_required


@market.route('/news')
@roles_required('user', 'player')
@login_required
def news():
    if not get_game_roles():
        abort(404)

    return render_template("market/news.html",
                           title='Новости')
