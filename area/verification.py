#  Nikulin Vasily © 2021
from flask import render_template

from area import area
from edu import edu
from market import market


@area.route('/yandex_58762f224fa898fc.html')
@market.route('/yandex_58762f224fa898fc.html')
@edu.route('/yandex_58762f224fa898fc.html')
def yandex_verification():
    return render_template('area/yandex_58762f224fa898fc.html')
