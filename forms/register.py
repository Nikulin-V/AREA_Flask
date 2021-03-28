from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Отчество', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    school = StringField('Учебное заведение', validators=[DataRequired()])
    role = SelectField('Роль', validators=[DataRequired()],
                       choices=['Ученик', 'Учитель', 'Родитель'])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    date_of_birth = DateField('Дата рождения')
    about = TextAreaField('О себе')
    submit = SubmitField('Войти')
