#  Nikulin Vasily © 2021
from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles, get_constant
from tools.tools import use_subdomains, game_running_required

marketplace_page = Blueprint('marketplace', __name__)
app = marketplace_page


@app.route('/marketplace', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}marketplace.html')
@login_required
@game_running_required
def marketplace(template):
    if not get_game_roles():
        abort(404)

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Торговая площадка')
