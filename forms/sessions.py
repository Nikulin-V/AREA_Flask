#  Nikulin Vasily © 2021

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, BooleanField


class SessionForm(FlaskForm):
    session = SelectField('Текущая фондовая биржа')
    submit = SubmitField('Готово ✅', default=False)


class NewSessionForm(FlaskForm):
    title = StringField('Имя новой фондовой биржи')
    submit = SubmitField('Создать фондовую биржу ✅', default=False)


class DeleteSessionForm(FlaskForm):
    accept = BooleanField('Подтвердить', default=False)
    submit = SubmitField('Удалить текущую фондовую биржу ❌')
