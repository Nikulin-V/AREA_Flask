#  Nikulin Vasily (c) 2021

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, BooleanField, SelectMultipleField


class CompanyManagementForm(FlaskForm):
    action = SelectField('Действие',
                         choices=['Добавить компанию', 'Изменить компанию', 'Удалить компанию',
                                  'Удалить все компании'])
    section = SelectField('Секция')
    new_section = StringField('Секция')
    company = SelectField('Компания')
    title = StringField('Название компании')
    user_submitted = 1
    accept_delete_all_companies = BooleanField('Подтвердить', default=False)
    authors = SelectMultipleField('Авторы', coerce=int)
    submit = SubmitField('Готово ✅')
