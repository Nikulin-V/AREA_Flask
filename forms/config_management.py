#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l, _
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, BooleanField, IntegerField, SelectField


class ConfigManagementForm(FlaskForm):
    game_run = BooleanField(_l('Игра идёт '
                               '(когда выключено - на торговой площадке показываются текущие '
                               'результаты игры)'))
    start_wallet_money = FloatField(_l('Начальный баланс на кошельке игрока'))
    fee = FloatField(_l('Комиссия от сделки '
                        '(умножается на сумму сделки для вычисления комиссии за 1 акцию)'))
    new_company_fee = FloatField(_l('Взнос за создание компании'))
    start_stocks = IntegerField(_l('Количество акций, которое игрок получает при создании '
                                   'компании'))
    month_duration = IntegerField(_l('Продолжительность 1 игрового месяца'))
    month_duration_unit = SelectField(_l('Ед. изм.'),
                                      choices=[_('Дни'), _('Часы'), _('Минуты'), _('Секунды')])
    property_tax = FloatField(_l('Процентная ставка налога на имущество'))
    income_tax = FloatField(_l('Процентная ставка подоходного налога'))
    submit = SubmitField(_l('Готово'))
