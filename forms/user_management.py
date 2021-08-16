#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField


class UserManagementForm(FlaskForm):
    user = SelectField(_l('Пользователь'
                          ' (Нажмите на поле и начните вводить фамилию нужного пользователя)'))
    game_role = SelectMultipleField(_l('Роли в текущей игре'),
                                    choices=[('Player', _l('Игрок')),
                                             ('Admin', _l('Администратор')),
                                             ('No roles', _l('Нет ролей')),
                                             ('Delete', _l('Удалить (Все акции и предложения на '
                                                           'торговой площадке переходят Вам)'))])
    submit = SubmitField(_l('Готово'))
