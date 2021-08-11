#  Nikulin Vasily © 2021
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField


class UserManagementForm(FlaskForm):

    user = SelectField('Пользователь'
                       ' (Нажмите на поле и начните вводить фамилию нужного пользователя)')
    game_role = SelectMultipleField('Роли в текущей игре',
                                    choices=[('Player', 'Игрок'),
                                             ('Admin', 'Администратор'),
                                             ('No roles', 'Нет ролей'),
                                             ('Delete', 'Удалить (Все акции и предложения на '
                                                        'торговой площадке переходят Вам)')])
    submit = SubmitField('Готово')
