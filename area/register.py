#  Nikulin Vasily © 2021
from flask import redirect, render_template, request
from flask_login import current_user, login_user

from area import area
from data import db_session
from data.roles import RolesUsers, Role
from data.sessions import Session
from data.users import User
from edu import edu
from forms.register import RegisterForm
from market import market
from tools.url import url


@area.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/profile')

    db_sess = db_session.create_session()

    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("area/register.html",
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   btn_label='Войти')

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("area/register.html",
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   btn_label='Войти')

        # noinspection PyArgumentList
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)

        roles = ['user', 'player']
        for role_name in roles:
            role = RolesUsers(
                user_id=user.id,
                role_id=db_sess.query(Role.id).filter(Role.name == role_name)
            )
            db_sess.add(role)

        db_sess.commit()
        login_user(user)
        session = db_sess.query(Session).get('77777777')
        session.players_ids = ';'.join(session.players_ids.split(';') + [str(current_user.id)])
        return redirect(url(request.args.get('redirect_page') or ".profile"))

    return render_template("area/register.html",
                           title='Регистрация',
                           form=form,
                           btn_label='Войти')


@market.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url('area.register') +
                    '?redirect_page=market.index')


@edu.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url('area.register') +
                    '?redirect_page=edu.index')
