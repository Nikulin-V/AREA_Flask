#  Nikulin Vasily © 2021
from flask import render_template, Blueprint
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from tools.tools import use_subdomains, get_subdomain

index_page = Blueprint('index', __name__)
app = index_page


@app.route('/')
@app.route('/index')
@use_subdomains(subdomains=['area', 'edu', 'market'])
@mobile_template('/{mobile/}index.html')
def index(template: str):
    template = get_subdomain() + template
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Главная')
