from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, PasswordField
from wtforms.validators import DataRequired


class UserManagementForm(FlaskForm):
    action = SelectField('Действие', choices=['Добавить пользователя', 'Удалить пользователя', 'Изменить пользователя'])
    user = SelectField('Пользователь')
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Отчество', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    game_role = StringField('Роли')
    submit = SubmitField('Готово ✅')
