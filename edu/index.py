#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from edu import edu


@edu.route('/')
@edu.route('/index')
@mobile_template('edu/{mobile/}index.html')
def index(template: str):
    return render_template(template,
                           title='Главная')
