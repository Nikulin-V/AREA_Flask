#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required

from edu import edu
from tools.tools import roles_required, roles_allowed


@edu.route('/classes')
@roles_required('user')
@roles_allowed('head_teacher', 'director')
@login_required
def classes():
    return render_template('edu/classes.html',
                           title='Классы')
