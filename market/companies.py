#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from market import market
from tools.tools import game_running_required


@market.route('/companies', methods=['GET', 'POST'])
@mobile_template('market/{mobile/}companies.html')
@login_required
@game_running_required
def companies(template):
    return render_template(template,
                           title='Компании')
