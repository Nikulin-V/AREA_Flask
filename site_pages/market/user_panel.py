#  Nikulin Vasily (c) 2021

#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.functions import get_game_roles, get_session_id
from data.offers import Offer
from data.sessions import Session
from data.stocks import Stock
from data.users import User
from forms.user_management import UserManagementForm
from tools import use_subdomains

user_panel_page = Blueprint('user-panel', __name__)
app = user_panel_page


# noinspection PyArgumentList
@app.route('/user-panel', methods=['GET', 'POST'])
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}user-panel.html')
@login_required
def user_panel(template, subdomain='market'):
    if 'Admin' not in get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    form = UserManagementForm()
    message = ''

    if form.is_submitted():
        session = db_sess.query(Session).get(get_session_id())
        session.admins_ids = str(session.admins_ids)
        session.players_ids = str(session.players_ids)
        if 'Admin' in form.game_role.data:
            if form.user.data not in session.admins_ids.split(';'):
                session.admins_ids = ';'.join(session.admins_ids.split(';') + [str(form.user.data)])
        if 'Player' in form.game_role.data:
            if form.user.data not in session.players_ids.split(';'):
                session.players_ids = ';'.join(
                    session.players_ids.split(';') + [str(form.user.data)])
        if 'No roles' in form.game_role.data:
            if form.user.data in session.admins_ids.split(';'):
                session.admins_ids = session.admins_ids.split(';')
                session.admins_ids.remove(str(form.user.data))
                session.admins_ids = ';'.join(session.admins_ids)
                db_sess.merge(session)
            if form.user.data in session.players_ids.split(';'):
                session.players_ids = session.players_ids.split(';')
                session.players_ids.remove(str(form.user.data))
                session.players_ids = ';'.join(session.players_ids)
                db_sess.merge(session)
        elif 'Delete' in form.game_role.data:
            if form.user.data in session.admins_ids.split(';'):
                session.admins_ids = session.admins_ids.split(';')
                session.admins_ids.remove(str(form.user.data))
                session.admins_ids = ';'.join(session.admins_ids)
                db_sess.merge(session)
            if form.user.data in session.players_ids.split(';'):
                session.players_ids = session.players_ids.split(';')
                session.players_ids.remove(str(form.user.data))
                session.players_ids = ';'.join(session.players_ids)
                db_sess.merge(session)
            offers = list(db_sess.query(Offer).filter(
                Offer.user_id == form.user.data,
                Offer.session_id == get_session_id()
            ).all())
            stocks = list(db_sess.query(Stock).filter(
                Stock.user_id == form.user.data,
                Stock.session_id == get_session_id()
            ).all())
            for item in offers + stocks:
                item.user_id = current_user.id
                db_sess.merge(item)

            message = 'Пользователь удалён из игры. Все его акции и предложения на торговой ' \
                      'площадке перешли в Вашу собственность. '
        db_sess.commit()
        roles = []
        if str(form.user.data) in str(session.admins_ids).split(';'):
            roles.append('Администратор')
        if str(form.user.data) in str(session.players_ids).split(';'):
            roles.append('Игрок')
        if not message:
            if roles:
                message = f'Текущие роли пользователя: {", ".join(roles)}.'
            else:
                message = 'У пользователя нет ролей.'

    form.user.choices = sorted(list(map(lambda x: (x[0], f'{x[1]} {x[2]}'),
                                        db_sess.query(User.id, User.surname, User.name))),
                               key=lambda x: x[1])
    if not form.user.data:
        form.user.data = form.user.choices[0]

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Панель управления пользователями',
                           message=message,
                           form=form)
