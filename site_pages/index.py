#  Nikulin Vasily (c) 2021

from flask import render_template, Blueprint
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles

index_page = Blueprint('index', __name__)
app = index_page


@app.route('/')
@app.route('/index')
@mobile_template('area/{mobile/}index.html')
def area_index(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Главная')


@app.route('/', subdomain='edu')
@app.route('/index', subdomain='edu')
@mobile_template('edu/{mobile/}index.html')
def edu_index(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Главная')


@app.route('/')
@app.route('/index')
@mobile_template('market/{mobile/}index.html')
def market_index(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Главная')
