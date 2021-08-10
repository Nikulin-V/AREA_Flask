#  Nikulin Vasily © 2021

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class UserAdminManagementForm(FlaskForm):
    action = SelectField('Действие', choices=['Добавить пользователя', 'Удалить пользователя',
                                              'Изменить пользователя'])
    user = SelectField('Пользователь')
    surname = StringField('Фамилия')
    name = StringField('Имя')
    patronymic = StringField('Отчество')
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    role = StringField('Роли (Введите роли пользователя через пробел (Ученик, Учитель, Админ) )')
    game_role = StringField('Роли в игре (Введите роли пользователя через пробел '
                            '(Игрок, Эксперт, Админ) )')
    submit = SubmitField('Готово')
