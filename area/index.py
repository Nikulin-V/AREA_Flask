#  Nikulin Vasily © 2021
from flask import render_template
from flask_babel import _

from area import area


@area.route('/')
@area.route('/index')
def index():
    return render_template("area/index.html",
                           title=_('Главная'))
