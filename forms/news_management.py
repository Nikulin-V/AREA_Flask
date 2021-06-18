from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class UserManagementForm(FlaskForm):
    action = SelectField('Действие', choices=['Добавить новость'])
    # TODO: Добавить действия: 'Удалить новость', 'Изменить новость'
    identifier = IntegerField('Номер')
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Готово ✅')
    author = SelectField('Автор', validators=[DataRequired()])
    picture = StringField('Ссылка на изображение')
