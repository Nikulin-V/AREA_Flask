#  Nikulin Vasily © 2021
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, BooleanField, IntegerField, SelectField


class ConfigManagementForm(FlaskForm):
    game_run = BooleanField('Игра идёт '
                            '(когда выключено - на торговой площадке показываются текущие '
                            'результаты игры)')
    start_wallet_money = FloatField('Начальный баланс на кошельке игрока')
    fee = FloatField('Комиссия от сделки '
                     '(умножается на сумму сделки для вычисления комиссии за 1 акцию)')
    new_company_fee = FloatField('Взнос за создание компании')
    start_stocks = IntegerField('Количество акций, которое игрок получает при создании компании')
    month_duration = IntegerField('Продолжительность 1 месяца')
    month_duration_unit = SelectField('Ед. изм.', choices=['Дни', 'Часы', 'Минуты', 'Секунды'])
    property_tax = FloatField('Процентная ставка налога на имущество')
    income_tax = FloatField('Процентная ставка подоходного налога')
    submit = SubmitField('Готово')
