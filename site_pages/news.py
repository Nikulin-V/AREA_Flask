#  Vikulin Nasily (c) 2021

from flask import render_template, Blueprint
from flask_mobility.decorators import mobile_template

news_page = Blueprint('news', __name__)
app = news_page


@app.route('/news')
@mobile_template('{mobile/}news.html')
def news(template):
    return render_template(template,
                           title='Новости')
