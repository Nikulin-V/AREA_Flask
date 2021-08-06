#  Nikulin Vasily © 2021

from flask import render_template, Blueprint, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data.functions import get_game_roles
from tools.tools import use_subdomains

news_page = Blueprint('news-page', __name__)
app = news_page


@app.route('/news')
@use_subdomains(subdomains=['market'])
@mobile_template('market/{mobile/}news.html')
@login_required
def news(template):
    if not get_game_roles():
        abort(404)

    return render_template(template,
                           game_role=get_game_roles(),
                           title='Новости')
