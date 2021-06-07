from flask_wtf import FlaskForm
from wtforms import SubmitField


class PurchaseForm(FlaskForm):
    accept = SubmitField('Подтвердить ✅')
    decline = SubmitField('Отклонить ❌')
