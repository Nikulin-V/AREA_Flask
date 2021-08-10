#  Nikulin Vasily © 2021
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.schools import School
from data.sessions import Session
from data.users import User
from edu import edu
from forms.register import RegisterForm
from app import area
from market import market
from tools.tools import get_subdomain


@area.route('/register', methods=['GET', 'POST'])
@mobile_template('/{mobile/}register.html')
def register(template: str):
    template = get_subdomain() + template

    if current_user.is_authenticated:
        return redirect('/profile')

    db_sess = db_session.create_session()

    form = RegisterForm()

    schools = sorted(list(map(lambda x: x[0], db_sess.query(School.title))))
    form.school.choices = schools

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(template,
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   btn_label='Войти')

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(template,
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   btn_label='Войти')

        # noinspection PyArgumentList
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            patronymic=form.patronymic.data,
            date_of_birth=form.date_of_birth.data,
            email=form.email.data,
            epos_login=form.epos_login.data,
            epos_password=form.epos_password.data,
            school_id=int(db_sess.query(School.id).
                          filter(School.title == form.school.data).first()[0]),
            role=form.role.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        session = db_sess.query(Session).get('77777777')
        session.players_ids = ';'.join(session.players_ids.split(';') + [str(current_user.id)])
        redirect(url_for(request.args.get('redirect_page')) or url_for("/profile"))

    return render_template(template,
                           title='Регистрация',
                           form=form,
                           btn_label='Войти')


@market.route('/register', methods=['GET', 'POST'])
def redirect_register():
    return redirect(url_for('area.register') + '?redirect_page=market.index')


@edu.route('/register', methods=['GET', 'POST'])
def redirect_register():
    return redirect(url_for('area.register') + '?redirect_page=edu.index')
