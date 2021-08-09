#  Nikulin Vasily © 2021

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, SelectField, StringField, FileField, TextAreaField
from wtforms.validators import DataRequired

from config import sectors


class CompanyManagementForm(FlaskForm):
    sector = SelectField('Отрасль', choices=sectors, default=sectors[0])
    title = StringField('Название компании', validators=[DataRequired()])
    description = TextAreaField('Описание')
    logo_url = FileField('Логотип',
                         validators=[FileAllowed(['jpg', 'png', 'bmp'],
                                                 'Только изображения в форматах jpg, png, bmp')])
    submit = SubmitField('Готово', default=False)
