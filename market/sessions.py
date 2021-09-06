#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required

from market import market
from tools.tools import roles_required


@market.route('/sessions', methods=['GET', 'POST'])
@roles_required('user', 'player')
@login_required
def sessions():
    return render_template("market/sessions.html",
                           title='Фондовые биржи')
