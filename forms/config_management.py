from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, BooleanField


class ConfigManagementForm(FlaskForm):
    fee = FloatField('Комиссия от сделки')
    game_run = BooleanField('Игра идёт')
    submit = SubmitField('Готово ✅')
