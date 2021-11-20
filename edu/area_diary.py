#  Nikulin Vasily © 2021
from datetime import date

from flask import render_template
from flask_login import login_required, current_user

from data import db_session
from data.classes import Group
from data.db_functions import repair_dependencies_students_and_groups
from data.homeworks import Homework
from data.students import Student
from edu import edu
from tools.tools import roles_required


@edu.route('/area-diary')
@roles_required('user', 'student')
@login_required
def area_diary():
    repair_dependencies_students_and_groups()
    db_sess = db_session.create_session()
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']
    schedule = dict()
    for day in days:
        schedule[day] = [['-', -1] for _ in range(8)]

    # Получаем группы ученика и составляем по ним расписание
    group_ids = list(db_sess.query(Student.group_id).filter(Student.user_id == current_user.id))
    for group_id in group_ids:
        group = db_sess.query(Group).get(group_id)
        for day_n, lesson_n in list(map(lambda x: (int(x[0]), int(x[1])),
                                        str(group.schedule).split(','))):
            schedule[days[day_n - 1]][lesson_n - 1][0] = group.subject
            schedule[days[day_n - 1]][lesson_n - 1][1] = group_id[0]

    # Убираем пустые уроки с конца
    for key in schedule.keys():
        try:
            while schedule[key][-1][0] == '-':
                schedule[key] = schedule[key][:-1]
        except IndexError:
            pass

    begin_date = date(2021, 5, 3)
    homework = dict()
    for day in days:
        homework[day] = [[] for _ in range(8)]
    for day_n in range(6):
        for lesson_n in range(len(schedule[days[day_n - 1]])):
            homeworks = list(map(lambda x: str(x[0]).capitalize(),
                                 db_sess.query(Homework.homework).filter(
                                     Homework.date == date(begin_date.year,
                                                           begin_date.month,
                                                           begin_date.day + day_n),
                                     Homework.lesson_number == lesson_n,
                                     Homework.group_id == schedule[days[day_n]][lesson_n - 1][1]
                                 )))
            if homeworks:
                homework[days[day_n]][lesson_n - 1] = homeworks
    dates = [str(begin_date.day + i).rjust(2, '0') for i in range(6)]
    return render_template("edu/area_diary.html",
                           title='Дневник AREA',
                           schedule=schedule,
                           homework=homework,
                           dates=dates,
                           days=days)
