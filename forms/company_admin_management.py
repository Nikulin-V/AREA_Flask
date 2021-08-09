#  Nikulin Vasily © 2021

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, BooleanField, SelectMultipleField


class CompanyAdminManagementForm(FlaskForm):
    action = SelectField('Действие',
                         choices=['Открыть компанию', 'Изменить компанию', 'Закрыть компанию',
                                  'Удалить все компании'])
    sector = SelectField('Отрасль')
    new_sector = StringField('Отрасль')
    company = SelectField('Компания')
    title = StringField('Название компании')
    user_submitted = 1
    accept_delete_all_companies = BooleanField('Подтвердить', default=False)
    authors = SelectMultipleField('Авторы', coerce=int)
    submit = SubmitField('Готово')
