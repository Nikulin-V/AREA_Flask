#  Nikulin Vasily (c) 2021
from flask import Blueprint, abort, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data.epos import EPOS

epos_diary_page = Blueprint('epos-diary', __name__)
app = epos_diary_page

epos = EPOS()


@app.route('/epos-diary')
@mobile_template('{mobile/}epos-diary.html')
@login_required
def epos_diary(template):
    if not current_user.is_authenticated:
        abort(401)

    if not (current_user.epos_login and current_user.epos_password):
        abort(403)

    epos_login = current_user.epos_login
    epos_password = current_user.epos_password
    epos.run(epos_login, epos_password)
    response = epos.get_schedule()
    response: list
    schedule = []

    if response == 'bad password':
        abort(403)
    elif response == 'timeout':
        abort(408)
    else:
        schedule = response

    return render_template(template,
                           title='Дневник ЭПОСа',
                           schedule=schedule)
