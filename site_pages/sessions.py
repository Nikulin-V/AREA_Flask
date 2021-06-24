#  Nikulin Vasily (c) 2021

from flask import render_template, Blueprint
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from config import PROFIT_PERCENT, GAME_RUN, START_STOCKS
from data import db_session
from data.config import Constant
from data.functions import get_game_roles, get_game_sessions
from data.sessions import Session
from data.users import User
from forms.sessions import SessionForm, NewSessionForm, DeleteSessionForm
from tools import generate_string

sessions_page = Blueprint('sessions-page', __name__)
app = sessions_page


# noinspection PyArgumentList
@app.route('/sessions', methods=['GET', 'POST'])
@mobile_template('{mobile/}sessions.html')
@login_required
def sessions(template):
    db_sess = db_session.create_session()
    form = SessionForm()
    form_new = NewSessionForm()
    form_delete = DeleteSessionForm()

    evaluate_sessions(form)

    if not form.session.data:
        session = db_sess.query(Session).get(current_user.game_session_id)
        if not session and form.session.choices:
            session = db_sess.query(Session).get(form.session.choices[0].split(' | ')[1])
        if session:
            form.session.data = f'{session.title} | {session.id}'

    if form_new.validate_on_submit() and form_new.title.data:
        new_session_id = generate_string(list(map(lambda x: x[0], db_sess.query(Session.id))))
        session = Session(
            id=new_session_id,
            title=form_new.title.data,
            admins_ids=str(current_user.id),
            players_ids=str(current_user.id)
        )
        db_sess.add(session)
        db_sess.commit()
        profit_percent = Constant(
            session_id=new_session_id,
            name='PROFIT_PERCENT',
            value=PROFIT_PERCENT
        )
        game_run = Constant(
            session_id=new_session_id,
            name='GAME_RUN',
            value=GAME_RUN
        )
        start_stocks = Constant(
            session_id=new_session_id,
            name='START_STOCKS',
            value=START_STOCKS
        )
        db_sess.add_all([profit_percent, game_run, start_stocks])
        db_sess.commit()
        form.session.data = f'{session.title} | {session.id}'
        form_new.title.data = ''
        user = db_sess.query(User).get(current_user.id)
        user.game_session_id = session.id
        db_sess.merge(user)
        db_sess.commit()

    elif form.validate_on_submit() and\
            form.session.data.split(' | ')[1] != current_user.game_session_id:
        session = form.session.data
        identifier = session.split(' | ')[1]
        user = db_sess.query(User).get(current_user.id)
        user.game_session_id = identifier
        db_sess.merge(user)
        db_sess.commit()
        form.session.data = session

    elif form_delete.validate_on_submit():
        if 'Admin' in get_game_roles():
            if form_delete.accept.data:
                form_delete.accept.data = False
                session = db_sess.query(Session).get(current_user.game_session_id)
                db_sess.delete(session)
                db_sess.commit()
                evaluate_sessions(form)
                user = db_sess.query(User).get(current_user.id)
                if form.session.choices:
                    session_id = form.session.choices[0].split(' | ')[1]
                    user.game_session_id = session_id
                    db_sess.merge(user)
                    db_sess.commit()

    evaluate_sessions(form)

    return render_template(template,
                           game_role=get_game_roles(form.session.choices[0].split(' | ')[1]
                                                    if form.session.choices else None),
                           form=form,
                           form_new=form_new,
                           form_delete=form_delete,
                           title='Игры')


def evaluate_sessions(form):
    data = get_game_sessions()
    sessions_list = []
    for session in data:
        sessions_list.append(f'{session.title} | {session.id}')

    form.session.choices = sessions_list
