#  Nikulin Vasily © 2021
from flask import render_template, abort
from flask_login import current_user, login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.functions import get_game_roles
from data.users import User
from forms.user_management import UserManagementForm
from app import area


# noinspection PyArgumentList
@area.route('/user-panel', methods=['GET', 'POST'])
@mobile_template('area/{mobile/}user-panel.html')
@login_required
def user_panel(template):
    if 'Admin' not in get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    form = UserManagementForm()
    message = ''

    if not form.action.data:
        form.action.data = 'Добавить пользователя'

    evaluate_form(form)

    if form.validate_on_submit() or (form.is_submitted() and not form.user.data):
        if form.action.data == 'Добавить пользователя':
            if form.surname.data and form.name.data and form.email.data and form.password.data:
                user = User(
                    surname=form.surname.data,
                    name=form.name.data,
                    patronymic=form.patronymic.data,
                    email=form.email.data,
                    game_role=form.game_role.data,
                    role=form.role.data
                )
                user.set_password(form.password.data)
                db_sess.add(user)
                db_sess.commit()
                evaluate_form(form)
                message = 'Пользователь добавлен'
        elif form.action.data == 'Удалить пользователя':
            if form.user.data and form.user.description != '!':
                surname, name, email = form.user.data.replace('|', '').split()
                user = db_sess.query(User).filter(
                    User.surname == surname,
                    User.name == name,
                    User.email == email
                ).first()
                if user:
                    db_sess.delete(user)
                    db_sess.commit()
                    evaluate_form(form)
                    form.user.data = form.user.choices[0]
                    surname, name, email = form.user.data.replace('|', '').split()
                    user = db_sess.query(User).filter(
                        User.surname == surname,
                        User.name == name,
                        User.email == email
                    ).first()
                    form.surname.data = user.surname
                    form.name.data = user.name
                    form.patronymic.data = user.patronymic
                    form.email.data = user.email
                    form.role.data = user.role
                    form.game_role.data = user.game_role
                    message = 'Пользователь удалён'
                else:
                    message = 'Пользователь с указанными данными не существует'
            else:
                form.user.data = form.user.choices[0]
        elif form.action.data == 'Изменить пользователя':
            if form.user.data:
                surname, name, email = form.user.data.replace('|', '').split()
                user = db_sess.query(User).filter(
                    User.surname == surname,
                    User.name == name,
                    User.email == email
                ).first()
                if form.email.data != email:
                    form.surname.data = user.surname
                    form.name.data = user.name
                    form.patronymic.data = user.patronymic
                    form.email.data = user.email
                    form.role.data = user.role
                    form.game_role.data = user.game_role
                elif user:
                    user.surname = form.surname.data
                    user.name = form.name.data
                    if form.patronymic.data:
                        user.patronymic = form.patronymic.data
                    if form.role.data == '':
                        user.role = None
                    else:
                        user.role = form.role.data
                    if form.game_role.data == '':
                        user.game_role = None
                    else:
                        user.game_role = form.game_role.data
                    if form.password.data:
                        user.set_password(form.password.data)
                    db_sess.merge(user)
                    db_sess.commit()
                    message = 'Пользователь изменён'
                    evaluate_form(form)
                    form.user.data = form.user.choices[0]
                    surname, name, email = form.user.data.replace('|', '').split()
                    user = db_sess.query(User).filter(
                        User.surname == surname,
                        User.name == name,
                        User.email == email
                    ).first()
                    form.surname.data = user.surname
                    form.name.data = user.name
                    form.patronymic.data = user.patronymic
                    form.email.data = user.email
                    form.role.data = user.role

                else:
                    message = 'Пользователь с указанными данными не существует'
            else:
                if not form.user.data:
                    form.user.data = form.user.choices[0]
                    surname, name, email = form.user.data.replace('|', '').split()
                    user = db_sess.query(User).filter(
                        User.surname == surname,
                        User.name == name,
                        User.email == email
                    ).first()
                    form.surname.data = user.surname
                    form.name.data = user.name
                    form.patronymic.data = user.patronymic
                    form.email.data = user.email
                    form.role.data = user.role

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Панель управления пользователями',
                           message=message,
                           form=form)


def evaluate_form(form):
    if form.user:
        db_sess = db_session.create_session()
        users = list(db_sess.query(User.surname, User.name, User.email).filter(
            User.game_session_id == current_user.game_session_id
        ))
        users = list(map(lambda x: x[0] + ' ' + x[1] + ' | ' + x[2], users))
        users.sort()
        form.user.choices = users
        if not form.user.data:
            form.user.default = form.user.choices[0]