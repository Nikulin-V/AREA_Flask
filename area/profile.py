#  Nikulin Vasily © 2021
from flask import render_template, redirect, request
from flask_login import login_required, current_user

from area import area
from data import db_session
from data.schools import School
from edu import edu
from forms.profile import ProfileForm
from market import market
from tools.tools import roles_allowed
from tools.url import url


@area.route('/profile', methods=['GET', 'POST'])
@login_required
@roles_allowed('user')
def profile():
    form = ProfileForm()
    db_sess = db_session.create_session()
    user = current_user

    schools = sorted(list(map(lambda x: x[0], db_sess.query(School.title))))
    form.school.choices = schools

    message = ''

    if form.validate_on_submit():
        message = "Сохранено"

        user.surname = form.surname.data
        user.name = form.name.data
        user.patronymic = form.patronymic.data
        user.email = form.email.data
        user.school_id = int(db_sess.query(School.id).filter(
            School.title == form.school.data).first()[0])
        user.role = form.role.data
        user.date_of_birth = form.date_of_birth.data
        user.about = form.about.data

        user.epos_login = form.epos_login.data
        if form.epos_password.data:
            user.epos_password = form.epos_password.data

        if form.old_password.data or form.password.data or form.password_again.data:
            if not form.old_password.data:
                message = "Введите старый пароль"
            elif not form.password.data:
                message = "Введите новый пароль"
            elif not form.password_again.data:
                message = "Повторите новый пароль"
            elif not user.check_password(form.old_password.data):
                message = "Неверный старый пароль"
            elif form.password.data != form.password_again.data:
                message = "Пароли не совпадают"
            else:
                user.set_password(form.password.data)

        db_sess.merge(user)
        db_sess.commit()

        if request.args.get('redirect_page'):
            return redirect(url(request.args.get('redirect_page')))

    school = db_sess.query(School.title).filter(
        School.id == user.school_id).first()
    if not school:
        school = ''
    else:
        school = school[0]

    date = current_user.date_of_birth
    if not date:
        date = ''
    else:
        date = date.strftime('%d.%m.%Y')

    return render_template("area/profile.html",
                           title='Профиль',
                           form=form,
                           message=message,
                           school=school,
                           date=date,
                           btn_label='Сохранить')


@market.route('/profile', methods=['GET', 'POST'])
def profile():
    return redirect(url('area.profile') +
                    '?redirect_page=market.index')


@edu.route('/profile', methods=['GET', 'POST'])
def profile():
    return redirect(url('area.profile') +
                    '?redirect_page=edu.index')
