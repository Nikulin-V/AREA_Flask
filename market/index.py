#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from market import market


@market.route('/')
@market.route('/index')
@mobile_template('market/{mobile/}index.html')
def index(template: str):
    return render_template(template,
                           title='Главная')
