#  Nikulin Vasily (c) 2021

from flask import render_template, Blueprint
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.db_functions import get_game_roles, get_game_sessions
from data.sessions import Session
from data.users import User
from forms.sessions import SessionForm, NewSessionForm, DeleteSessionForm
from tools import generate_string

sessions_page = Blueprint('sessions-page', __name__)
app = sessions_page


@app.route('/sessions', methods=['GET', 'POST'])
@mobile_template('{mobile/}sessions.html')
@login_required
def sessions(template):
    db_sess = db_session.create_session()
    form = SessionForm()
    form_new = NewSessionForm()
    form_delete = DeleteSessionForm()

    data = get_game_sessions()
    sessions_list = []
    for session in data:
        sessions_list.append(f'{session.title} | {session.id}')

    form.session.choices = sessions_list

    if not form.session.data:
        session = db_sess.query(Session).get(current_user.game_session_id)
        form.session.data = f'{session.title} | {session.id}'

    print(form.session.data,
          form.session.choices)
    if form.validate_on_submit():
        session = form.session.data
        identifier = session.split(' | ')[1]
        user = db_sess.query(User).get(current_user.id)
        user.game_session_id = identifier
        db_sess.merge(user)
        db_sess.commit()
        form.session.data = session

    if form_new.validate_on_submit():
        if form_new.title.data:
            id = generate_string(list(map(lambda x: x[0], db_sess.query(Session.id))))
            session = Session(
                id=id,
                title=form_new.title.data,
                admins_ids=str(current_user.id),
                players_ids=str(current_user.id)
            )
            db_sess.add(session)
            db_sess.commit()
            form.session.data = f'{session.title} | {session.id}'
            user = db_sess.query(User).get(current_user.id)
            user.game_session_id = session.id
            db_sess.merge(user)
            db_sess.commit()

    if form_delete.validate_on_submit():
        if 'Admin' in get_game_roles():
            if form_delete.accept.data:
                session = db_sess.query(Session).get(current_user.game_session_id)
                db_sess.delete(session)
                db_sess.commit()

    return render_template(template,
                           game_role=get_game_roles(),
                           form=form,
                           form_new=form_new,
                           form_delete=form_delete,
                           title='Игры')
