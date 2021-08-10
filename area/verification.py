#  Nikulin Vasily © 2021
from flask import render_template, send_file

from app import area


@area.route('/yandex_58762f224fa898fc.html')
def yandex_verification():
    return render_template('yandex_58762f224fa898fc.html')


@area.route('/.well-known/pki-validation/98E7C8AF09D499DE1DF3015280BFC66A.txt')
def ssl_verification():
    return send_file('98E7C8AF09D499DE1DF3015280BFC66A.txt')
