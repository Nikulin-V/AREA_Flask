#  Nikulin Vasily © 2021
from flask import render_template, request
from flask_login import login_required

from edu import edu
from tools.tools import roles_required, roles_allowed


@edu.route('/workload')
@roles_required('user')
@roles_allowed('head_teacher', 'director')
@login_required
def workload():
    classNumber = request.args.get('classNumber')
    classLetter = request.args.get('classLetter')
    return render_template('edu/workload.html',
                           title=f'Почасовая нагрузка {classNumber}{classLetter}')
