#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField(_l('Фамилия'), validators=[DataRequired()])
    name = StringField(_l('Имя'), validators=[DataRequired()])
    patronymic = StringField(_l('Отчество'))
    email = EmailField(_l('Почта'), validators=[DataRequired()])
    school = SelectField(_l('Учебное заведение'))
    role = SelectField(_l('Роль'), validators=[DataRequired()],
                       choices=[_l('Ученик'), _l('Учитель'), _l('Родитель')])
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    password_again = PasswordField(_l('Повторите пароль'), validators=[DataRequired()])
    epos_login = StringField(_l('Логин / Email для входа в ЭПОС.Школа'))
    epos_password = PasswordField(_l('Пароль для входа в ЭПОС.Школа'))
    date_of_birth = DateField(_l('Дата рождения в формате 01.01.1970'), format='%d.%m.%Y')
    about = StringField(_l('О себе'))
    submit = SubmitField()
