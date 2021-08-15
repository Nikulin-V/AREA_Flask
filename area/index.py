#  Nikulin Vasily © 2021
from flask import render_template

from area import area


@area.route('/')
@area.route('/index')
def index():
    return render_template("area/index.html",
                           title='Главная')
