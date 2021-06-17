#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

from data import db_session
from data.config import Constant
from data.users import User
from forms.config_management import ConfigManagementForm
from forms.user_management import UserManagementForm

user_panel_page = Blueprint('control-panel', __name__)
app = user_panel_page


@app.route('/config-panel', methods=['GET', 'POST'])
@mobile_template('{mobile/}config-panel.html')
def user_panel(template):
    db_sess = db_session.create_session()

    form = ConfigManagementForm()
    message = ''

    if form.validate_on_submit():
        if form.fee.data:
            fee = db_sess.query(Constant).filter(Constant.name == 'PROFIT_PERCENT').first()
            fee.
            db_sess.merge(fee)

    return render_template(template,
                           title='Панель управления',
                           message=message,
                           form=form)
