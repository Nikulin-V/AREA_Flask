#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from market import market
from tools.tools import game_running_required


@market.route('/marketplace', methods=['GET', 'POST'])
@mobile_template('market/{mobile/}marketplace.html')
@login_required
@game_running_required
def marketplace(template):
    if not get_game_roles():
        abort(404)

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Торговая площадка')
