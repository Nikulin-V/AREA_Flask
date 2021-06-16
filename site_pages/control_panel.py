#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

from data import db_session
from data.users import User
from forms.user_management import UserManagementForm

control_panel_page = Blueprint('control-panel', __name__)
app = control_panel_page


@app.route('/control-panel', methods=['GET', 'POST'])
@mobile_template('{mobile/}control-panel.html')
def control_panel(template):
    db_sess = db_session.create_session()

    form = UserManagementForm()
    message = ''

    if not form.action.data:
        form.action.data = 'Добавить пользователя'

    evaluate_form(form)

    if form.validate_on_submit():
        if form.action.data == 'Добавить пользователя':
            if form.surname.data and form.name.data and form.patronymic.data and form.email.data and form.password.data:
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
                message = 'Пользователь добавлен'
        elif form.action.data == 'Удалить пользователя':
            user = db_sess.query(User).filter(
                User.surname == form.surname.data,
                User.name == form.name.data,
                User.patronymic == form.patronymic.data,
                User.email == form.email.data
            ).first()
            if user:
                db_sess.delete(user)
                db_sess.commit()
            else:
                message = 'Пользователь с указанными данными не существует'
        elif form.action.data == 'Изменить пользователя':
            if form.user.data:
                form.surname.data, form.name.data, form.email.data = \
                    form.user.data.split()
                user = db_sess.query(User).filter(
                    User.surname == form.surname.data,
                    User.name == form.name.data,
                    User.email == form.email.data
                ).first()
                if user:
                    user.email = form.email.data
                    user.surname = form.surname.data
                    user.name = form.name.data
                    user.role = form.role.data
                    user.game_role = form.game_role.data
                    if form.password.data:
                        user.set_password(form.password.data)
                    db_sess.merge(user)
                    db_sess.commit()
                else:
                    message = 'Пользователь с указанными данными не существует'
            else:
                users = list(db_sess.query(User.surname, User.name, User.email).filter(
                    User.game_role is not None
                ))
                users = list(map(lambda x: x[0] + ' ' + x[1] + ' | ' + x[2], users))
                form.user.choices = users
                if not form.user.data:
                    form.user.data = form.user.choices[0]

    return render_template(template,
                           title='Панель управления',
                           message=message,
                           form=form)


def evaluate_form(form):

    if form.user:
        db_sess = db_session.create_session()
        users = list(db_sess.query(User.surname, User.name, User.email).filter(
            User.game_role is not None
        ))
        users = list(map(lambda x: ' '.join(x), users))
        form.user.choices = users
        if not form.user.data:
            form.user.data = form.user.choices[0]
