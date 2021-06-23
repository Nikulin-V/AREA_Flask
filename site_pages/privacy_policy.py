#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

from data.db_functions import get_game_roles

privacy_policy_page = Blueprint('privacy-policy', __name__)
app = privacy_policy_page


@app.route('/privacy-policy')
@mobile_template('{mobile/}privacy-policy.html')
def privacy_policy(template):
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Политика конфиденциальности')
