#  Nikulin Vasily © 2021
from flask import render_template
from flask_babel import _

from market import market


@market.route('/')
@market.route('/index')
def index():
    return render_template("market/index.html",
                           title=_('Главная'))
