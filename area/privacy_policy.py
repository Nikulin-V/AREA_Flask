#  Nikulin Vasily © 2021
from flask import render_template
from flask_babel import _

from area import area


@area.route('/privacy-policy')
def privacy_policy():
    return render_template("area/privacy_policy.html",
                           title=_('Политика конфиденциальности'))
