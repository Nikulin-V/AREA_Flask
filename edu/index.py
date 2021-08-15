#  Nikulin Vasily © 2021
from flask import render_template

from edu import edu


@edu.route('/')
@edu.route('/index')
def index():
    return render_template("edu/index.html",
                           title='Главная')
