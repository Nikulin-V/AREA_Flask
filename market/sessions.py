#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from market import market


@market.route('/sessions', methods=['GET', 'POST'])
@mobile_template('market/{mobile/}sessions.html')
@login_required
def sessions(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Фондовые биржи')
