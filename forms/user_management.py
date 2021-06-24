from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField


class UserManagementForm(FlaskForm):

    user = SelectField('Пользователь'
                       ' (Нажмите на поле и начните вводить фамилию нужного пользователя')
    game_role = SelectMultipleField('Роли в текущей игре',
                                    choices=[('Player', 'Игрок'),
                                             ('Admin', 'Администратор'),
                                             ('None', 'Нет ролей')])
    submit = SubmitField('Готово ✅')
