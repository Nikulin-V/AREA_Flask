#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from market import market
from tools.tools import game_running_required


@market.route('/companies-management')
@mobile_template('market/{mobile/}companies-management.html')
@login_required
@game_running_required
def stockholders_voting(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Управление компаниями')
