#  Nikulin Vasily © 2021

from flask import render_template, Blueprint

from tools.tools import use_subdomains

yandex_verification_page = Blueprint('yandex-verification', __name__)
app = yandex_verification_page


@app.route('/yandex_58762f224fa898fc.html')
@use_subdomains(subdomains=['area', 'edu', 'market'])
def index():
    return render_template('yandex_58762f224fa898fc.html')
