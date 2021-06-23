#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.config import Constant
from data.db_functions import get_game_roles
from forms.config_management import ConfigManagementForm

game_panel_page = Blueprint('game-panel', __name__)
app = game_panel_page


@app.route('/game-panel', methods=['GET', 'POST'])
@mobile_template('{mobile/}game-panel.html')
@login_required
def game_panel(template):
    if 'Admin' not in get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    form = ConfigManagementForm()
    message = ''

    if form.validate_on_submit():
        if form.fee.data:
            fee = db_sess.query(Constant).filter(Constant.name == 'PROFIT_PERCENT').first()
            fee.value = form.fee.data
            db_sess.merge(fee)
        game_run = db_sess.query(Constant).filter(Constant.name == 'GAME_RUN').first()
        game_run.value = 1 if form.game_run.data else 0
        db_sess.merge(game_run)
        db_sess.commit()
        message = 'Сохранено'

    if not form.fee.data:
        form.fee.data = db_sess.query(Constant.value).filter(
            Constant.name == 'PROFIT_PERCENT').first()[0]

    if not form.game_run.data:
        form.game_run.data = db_sess.query(Constant.value).filter(
            Constant.name == 'GAME_RUN').first()[0]

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Управление игровым процессом',
                           message=message,
                           form=form)
