from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import NumberRange


class StocksForm(FlaskForm):
    action = SelectField('Действие', choices=['Купить', 'Продать', 'Отменить продажу',
                                              'Инвестировать'])
    section = SelectField('Секция')
    company = SelectField('Проект')
    user = SelectField('Пользователь')
    amount = FloatField('Сумма инвестиции')
    stocks = IntegerField('Количество акций', default=0, validators=[NumberRange(min=0, max=100)])
    price = IntegerField('Цена за одну акцию', default=1, validators=[NumberRange(min=1, max=100)])
    submit = SubmitField('Готово ✅')
