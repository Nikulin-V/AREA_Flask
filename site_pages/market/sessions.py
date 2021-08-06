#  Nikulin Vasily © 2021
from flask import render_template, Blueprint
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from tools.tools import use_subdomains

sessions_page = Blueprint('sessions-page', __name__)
app = sessions_page


@app.route('/', methods=['GET', 'POST'])
@app.route('/sessions', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}sessions.html')
@login_required
def sessions(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Фондовые биржи')
