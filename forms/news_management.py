from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, TextAreaField, IntegerField


class UserManagementForm(FlaskForm):
    action = SelectField('Действие', choices=['Добавить новость', 'Удалить новость',
                                              'Изменить новость'])
    identifier = IntegerField('Номер')
    title = StringField('Заголовок')
    text = TextAreaField('Текст')
    submit = SubmitField('Готово ✅')
    author = SelectField('Автор')
    picture = StringField('Ссылка на изображение')
