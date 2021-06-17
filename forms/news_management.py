from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, TextAreaField


class UserManagementForm(FlaskForm):
    action = SelectField('Действие', choices=['Добавить новость', 'Удалить новость',
                                              'Изменить новость'])
    identifier = StringField('Номер')
    title = StringField('Заголовок')
    text = TextAreaField('Текст')
    submit = SubmitField('Готово ✅')
    author = SelectField('Автор')
