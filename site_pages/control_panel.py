#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

from forms.user_management import UserManagementForm

control_panel_page = Blueprint('control-panel', __name__)
app = control_panel_page


@app.route('/control-panel')
@mobile_template('{mobile/}control-panel.html')
def control_panel(template):
    form = UserManagementForm()



    return render_template(template,
                           title='Панель управления',
                           form=form)
