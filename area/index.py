#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from area import area


@area.route('/')
@area.route('/index')
@mobile_template('area/{mobile/}index.html')
def index(template: str):
    return render_template(template,
                           title='Главная')
