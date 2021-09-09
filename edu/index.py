#  Nikulin Vasily © 2021
from flask import render_template

from edu import edu
from tools.tools import roles_allowed


@edu.route('/')
@edu.route('/index')
@roles_allowed('student', 'teacher', 'head_teacher')
def index():
    return render_template("edu/index.html",
                           title='Главная')
