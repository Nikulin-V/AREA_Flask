#  Nikulin Vasily © 2021
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from flask_mobility.decorators import mobile_template

from area import area
from market import market
from edu import edu

from data import db_session
from data.users import User
from forms.login import LoginForm
from tools.tools import get_subdomain


@area.route('/login', methods=['GET', 'POST'])
@mobile_template('/{mobile/}login.html')
def login(template: str):
    template = get_subdomain() + template

    if current_user.is_authenticated:
        return redirect(url_for('.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user: User
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template(template,
                                   title='Авторизация',
                                   message="Вы не зарегистрированы в системе",
                                   form=form)
        if user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for(request.args.get('redirect_page')) or url_for("/index"))
        return render_template(template,
                               title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template(template,
                           title='Авторизация',
                           form=form)


@market.route('/login', methods=['GET', 'POST'])
def redirect_login():
    return redirect(url_for('area.login') + '?redirect_page=market.index')


@edu.route('/login', methods=['GET', 'POST'])
def redirect_login():
    return redirect(url_for('area.login') + '?redirect_page=edu.index')


@area.route('/logout')
@market.route('/logout')
@edu.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")
