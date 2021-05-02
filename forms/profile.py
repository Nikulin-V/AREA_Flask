from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    school = StringField('Учебное заведение', validators=[DataRequired()])
    role = SelectField('Роль', validators=[DataRequired()],
                       choices=['Ученик', 'Учитель', 'Родитель'])
    old_password = PasswordField('Старый пароль')
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    epos_login = StringField('Логин / Email для входа в ЭПОС.Школа', validators=[DataRequired()])
    epos_password = PasswordField('Пароль для входа в ЭПОС.Школа')
    date_of_birth = DateField('Дата рождения', format='%d.%m.%Y')
    about = StringField('О себе')
    submit = SubmitField()
