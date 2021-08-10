#  Nikulin Vasily © 2021
from flask import render_template

from app import area


@area.route('/yandex_58762f224fa898fc.html')
def yandex_verification():
    return render_template('yandex_58762f224fa898fc.html')
