#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField(_l('Почта'),
                       validators=[DataRequired(_l('Вы пропустили это поле'))])
    password = PasswordField(_l('Пароль'),
                             validators=[DataRequired(_l('Вы пропустили это поле'))])
    remember_me = BooleanField(_l('Запомнить меня'))
    submit = SubmitField(_l('Войти'))
