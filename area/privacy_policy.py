#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from area import area


@area.route('/privacy-policy')
@mobile_template('area/{mobile/}privacy-policy.html')
def privacy_policy(template: str):
    return render_template(template,
                           title='Политика конфиденциальности')
