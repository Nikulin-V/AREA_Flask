#  Nikulin Vasily © 2021
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    email = EmailField('Почта', validators=[DataRequired()])
    school = SelectField('Учебное заведение')
    role = SelectField('Роль', validators=[DataRequired()],
                       choices=['Ученик', 'Учитель', 'Родитель'])
    old_password = PasswordField('Старый пароль')
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    epos_login = StringField('Логин / Email для входа в ЭПОС.Школа')
    epos_password = PasswordField('Пароль для входа в ЭПОС.Школа')
    date_of_birth = DateField('Дата рождения в формате 01.01.1970', format='%d.%m.%Y')
    about = StringField('О себе')
    submit = SubmitField()
