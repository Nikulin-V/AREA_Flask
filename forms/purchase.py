from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, IntegerField


class PurchaseForm(FlaskForm):
    project = TextField('gg')
    stocks = IntegerField('12')
    price = IntegerField('24')
    accept = SubmitField('Подтвердить ✅')
    decline = SubmitField('Отклонить ❌')
