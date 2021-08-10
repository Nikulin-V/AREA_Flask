#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from area import area
from market import market
from edu import edu

from data.functions import get_game_roles

from tools.tools import get_subdomain


@area.route('/')
@area.route('/index')
@market.route('/')
@market.route('/index')
@edu.route('/')
@edu.route('/index')
@mobile_template('/{mobile/}index.html')
def index(template: str):
    template = get_subdomain() + template
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Главная')
