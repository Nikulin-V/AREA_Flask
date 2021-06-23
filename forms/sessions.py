from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, BooleanField


class SessionForm(FlaskForm):
    session = SelectField('Текущая игра')
    submit = SubmitField('Готово ✅', default=False)


class NewSessionForm(FlaskForm):
    title = StringField('Имя новой игры')
    submit = SubmitField('Создать игру ✅', default=False)


class DeleteSessionForm(FlaskForm):
    accept = BooleanField('Подтвердить', default=False)
    submit = SubmitField('Удалить текущую игру ❌')
