#  Nikulin Vasily © 2021
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, SelectField, StringField, FileField, TextAreaField
from wtforms.validators import DataRequired

from config import sectors


class CompanyManagementForm(FlaskForm):
    sector = SelectField(_l('Отрасль'), choices=sectors, default=sectors[0])
    title = StringField(_l('Название компании'),
                        validators=[DataRequired(_l('Вы пропустили это поле'))])
    description = TextAreaField(_l('Описание'))
    logo_url = FileField(_l('Логотип'),
                         validators=[
                             FileAllowed(['jpg', 'png', 'bmp'],
                                         _l('Только изображения в форматах jpg, png, bmp'))
                         ])
    submit = SubmitField(_l('Готово'), default=False)
