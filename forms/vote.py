from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import NumberRange


class VoteForm(FlaskForm):
    sector = SelectField('Отрасль')
    company = SelectField('Компания')
    points = IntegerField('Очки', default=0, validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Голосовать ✅')
    user = None
