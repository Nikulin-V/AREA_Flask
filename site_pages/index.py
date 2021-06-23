#  Nikulin Vasily (c) 2021

from flask import render_template, Blueprint
from flask_mobility.decorators import mobile_template

from data.db_functions import get_game_roles

index_page = Blueprint('index', __name__)
app = index_page


@app.route('/')
@app.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Главная')
