#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, BooleanField, SelectMultipleField


class CompanyAdminManagementForm(FlaskForm):
    action = SelectField('Действие',
                         choices=[_l('Открыть компанию'), _l('Изменить компанию'),
                                  _l('Закрыть компанию'), _l('Удалить все компании')])
    sector = SelectField(_l('Отрасль'))
    new_sector = StringField(_l('Отрасль'))
    company = SelectField(_l('Компания'))
    title = StringField(_l('Название компании'))
    user_submitted = 1
    accept_delete_all_companies = BooleanField(_l('Подтвердить'), default=False)
    authors = SelectMultipleField(_l('Авторы'), coerce=int)
    submit = SubmitField(_l('Готово'))
