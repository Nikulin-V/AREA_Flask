#  Nikulin Vasily © 2021
from flask import render_template
from flask_babel import _
from flask_login import login_required

from market import market


@market.route('/sessions', methods=['GET', 'POST'])
@login_required
def sessions():
    return render_template("market/sessions.html",
                           title=_('Фондовые биржи'))
