#  Nikulin Vasily © 2021
from flask import Blueprint, render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from tools.tools import use_subdomains

companies_management_page = Blueprint('companies-management-page', __name__)
app = companies_management_page


@app.route('/companies-management')
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}companies-management.html')
@login_required
def stockholders_voting(template):

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Управление компаниями')



