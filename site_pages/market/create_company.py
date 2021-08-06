#  Nikulin Vasily © 2021

from flask import Blueprint, render_template, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles, get_constant
from tools.tools import use_subdomains

my_companies_page = Blueprint('my-companies', __name__)
app = my_companies_page


@app.route('/create-company', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}create-company.html')
@login_required
def my_companies(template):
    if not get_game_roles():
        abort(404)

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Открыть компанию',
                           new_company_fee=get_constant('NEW_COMPANY_FEE'))
