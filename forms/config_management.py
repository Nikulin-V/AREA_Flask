#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, BooleanField, IntegerField


class ConfigManagementForm(FlaskForm):
    game_run = BooleanField(_l('Игра идёт '
                               '(когда выключено - на торговой площадке показываются текущие '
                               'результаты игры)'))
    start_wallet_money = FloatField(_l('Начальный баланс на кошельке игрока'))
    fee = FloatField(_l('Комиссия от сделки '
                        '(умножается на сумму сделки для вычисления комиссии за 1 акцию)'))
    new_company_fee = FloatField(_l('Взнос за создание компании'))
    start_stocks = IntegerField(
        _l('Количество акций, которое игрок получает при создании компании'))
    submit = SubmitField(_l('Готово'))
