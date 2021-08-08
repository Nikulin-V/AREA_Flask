#  Nikulin Vasily © 2021

import os

from flask import Flask, render_template, redirect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mobility.decorators import mobile_template
from flask_mobility.mobility import Mobility
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from api import api, sock
from data import db_session
from data.users import User
from site_pages import pages_blueprints
from tools.tools import use_subdomains, get_subdomain

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.me.readonly']

app = Flask(__name__, subdomain_matching=True)
app.config['SECRET_KEY'] = 'area_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
async_mode = None
socket_ = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

for blueprint in pages_blueprints:
    app.register_blueprint(blueprint)

app.register_blueprint(api)
socket_ = sock.init_io(socket_)
Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/database.sqlite')

port = int(os.environ.get('PORT', 80))


def main():
    socket_.run(app, host='0.0.0.0', port=port, debug=True)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/secrets-of-literacy')
def secrets_of_literacy():
    return redirect('https://secrets-of-literacy.wixsite.com/website')


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(408)
@app.errorhandler(500)
@mobile_template('/{mobile/}error-page.html')
@use_subdomains(subdomains=['', 'area', 'market', 'edu'])
def page_not_found(error, template: str):
    template = get_subdomain() + template
    messages = {
        401: ['Вы не вошли в систему',
              'Через несколько секунд Вы будете направлены на страницу авторизации'],
        403: ['Ошибка при авторизации в ЭПОС.Школа',
              'Попробуйте ещё раз. При повторном возникновении ошибки проверьте пароль от '
              'ЭПОС.Школа и обновите его в профиле'],
        404: ['Страница не найдена',
              'Проверьте правильность введённого адреса'],
        408: ['Превышено время ожидания',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
        500: ['Ошибка на стороне сайта',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
    }

    return render_template(template,
                           code=error.code,
                           title=messages[error.code][0],
                           message=messages[error.code][1])


if __name__ == '__main__':
    main()
