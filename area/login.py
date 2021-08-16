#  Nikulin Vasily © 2021
from flask import redirect, render_template, request
from flask_babel import _
from flask_login import current_user, login_user, login_required, logout_user

from area import area
from data import db_session
from data.users import User
from edu import edu
from forms.login import LoginForm
from market import market
from tools.url import url


@area.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url('.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user: User
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template("area/login.html",
                                   title=_('Авторизация'),
                                   message=_("Вы не зарегистрированы в системе"),
                                   form=form)
        if user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url(request.args.get('redirect_page') or ".index"))
        return render_template("area/login.html",
                               title=_('Авторизация'),
                               message=_("Неправильный логин или пароль"),
                               form=form)
    return render_template("area/login.html",
                           title=_('Авторизация'),
                           form=form)


@market.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url('area.login') +
                    '?redirect_page=market.index')


@edu.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url('area.login') +
                    '?redirect_page=edu.index')


@area.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url('area.login'))


@market.route('/logout')
@edu.route('/logout')
def logout():
    return redirect(url('area.logout'))
