#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class UserAdminManagementForm(FlaskForm):
    action = SelectField(_l('Действие'), choices=[_l('Добавить пользователя'),
                                                  _l('Удалить пользователя'),
                                                  _l('Изменить пользователя')])
    user = SelectField(_l('Пользователь'))
    surname = StringField(_l('Фамилия'))
    name = StringField(_l('Имя'))
    patronymic = StringField(_l('Отчество'))
    email = EmailField(_l('Почта'))
    password = PasswordField(_l('Пароль'))
    role = StringField(
        _l('Роли (Введите роли пользователя через пробел (Ученик, Учитель, Админ) )'))
    game_role = StringField(_l('Роли в игре (Введите роли пользователя через пробел '
                               '(Игрок, Эксперт, Админ) )'))
    submit = SubmitField(_l('Готово'))
