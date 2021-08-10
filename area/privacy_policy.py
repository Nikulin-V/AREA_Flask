#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from app import area
from edu import edu
from market import market
from tools.tools import get_subdomain


@area.route('/privacy-policy')
@market.route('/privacy-policy')
@edu.route('/privacy-policy')
@mobile_template('/{mobile/}privacy-policy.html')
def privacy_policy(template: str):
    template = get_subdomain() + template
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Политика конфиденциальности')
