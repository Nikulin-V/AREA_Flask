#  Nikulin Vasily (c) 2021
from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.db_functions import repair_dependencies_students_and_groups
from data.groups import Group
from data.homeworks import Homework
from data.students import Student

area_diary_page = Blueprint('area-diary', __name__)
app = area_diary_page


@app.route('/area-diary', subdomain='edu')
@mobile_template('{mobile/}area-diary.html')
@login_required
def area_diary(template):
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
    return render_template(template,
                           title='Дневник AREA',
                           schedule=schedule,
                           homework=homework,
                           dates=dates,
                           days=days)
