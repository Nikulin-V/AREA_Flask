#  Nikulin Vasily © 2021
from flask import Blueprint, render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from tools.tools import use_subdomains

companies_page = Blueprint('companies-voting', __name__)
app = companies_page


@app.route('/companies', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}companies.html')
@login_required
def companies_voting(template):

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Компании')
