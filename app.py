#  Nikulin Vasily © 2021
import os

import eventlet
from flask import Flask, redirect, Blueprint
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_mobility.mobility import Mobility
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

import area
import edu
import market
from config import SERVER_NAME, SCHEME
from data import db_session
from data.functions import get_game_roles
from data.users import User
from tools.admin import connect_models
from tools.scheduler import Scheduler
from tools.url import url

eventlet.monkey_patch()

app = Flask(__name__, subdomain_matching=True)
app.config.update(
    SERVER_NAME=SERVER_NAME,
    SECRET_KEY='area_secret_key',
    SQLALCHEMY_DATABASE_URI='sqlite:///db/database.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_DOMAIN=SERVER_NAME,
    SESSION_COOKIE_HTTPONLY=False,
    MAX_CONTENT_LENGTH=32 * 1024 * 1024,
    PREFERRED_URL_SCHEME=SCHEME
)
app.config.from_pyfile('config-extended.py')

socket_ = SocketIO(app, cors_allowed_origins="*")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = Scheduler()
mail = Mail(app)

Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.globals.update(url=url)
app.jinja_env.globals.update(game_role=get_game_roles)
app.jinja_env.globals.update(has_role=get_game_roles)
db_session.global_init('db/database.sqlite')


def main():
    port = int(os.environ.get('PORT', 443 if SCHEME == 'https' else 80))
    socket_.run(app, host='0.0.0.0', port=port, keyfile='private.key', certfile='certificate.crt')


def add_admin_panel():
    admin_bp = Blueprint('admin-panel', __name__, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix="/admin")

    admin = Admin(app, base_template='admin/master-extended.html')
    connect_models(admin)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/secrets-of-literacy')
def secrets_of_literacy():
    return redirect('https://secrets-of-literacy.wixsite.com/website')


if __name__ == '__main__':
    print('https://area-146.ru')
    add_admin_panel()

    services = [area.area, market.market, edu.edu]
    for service in services:
        app.register_blueprint(service)

    sockets = [area.socket, market.socket, edu.socket]
    for socket in sockets:
        socket_ = socket.init_io(socket_)

    main()
