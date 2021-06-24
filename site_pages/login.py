#  Nikulin Vasily (c) 2021
from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_user, login_required, logout_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.users import User
from forms.login import LoginForm

login_page = Blueprint('login', __name__)
app = login_page


@app.route('/login', methods=['GET', 'POST'])
@mobile_template('{mobile/}login.html')
def login(template):
    if current_user.is_authenticated:
        return redirect('/profile')

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
            return redirect("/sessions")
        return render_template(template,
                               title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template(template,
                           title='Авторизация',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")
