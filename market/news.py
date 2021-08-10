#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from market import market

@market.route('/news')
@mobile_template('market/{mobile/}news.html')
@login_required
def news(template):
    if not get_game_roles():
        abort(404)

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Новости')
