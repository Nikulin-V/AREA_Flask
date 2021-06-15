#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

privacy_policy_page = Blueprint('privacy-policy', __name__)
app = privacy_policy_page


@app.route('/privacy-policy')
@mobile_template('{mobile/}privacy-policy.html')
def privacy_policy(template):
    return render_template(template,
                           title='Политика конфиденциальности')
