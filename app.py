#  Nikulin Vasily © 2021
import os

from flask import Flask, redirect, url_for, Blueprint
from flask_admin import AdminIndexView, expose, Admin, helpers
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_mobility.mobility import Mobility
from flask_security import SQLAlchemyUserDatastore, Security, logout_user
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

import area
import edu
import market
from config import SERVER_NAME, SCHEME
from data import db_session
from data.functions import get_game_roles
from data.role import Role
from data.users import User
from tools.admin import connect_models
from tools.scheduler import Scheduler
from tools.url import url

app = Flask(__name__, subdomain_matching=True)
app.config.update(
    SERVER_NAME=SERVER_NAME,
    SECRET_KEY='area_secret_key',
    SQLALCHEMY_DATABASE_URI='sqlite:///db/database.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_DOMAIN=SERVER_NAME,
    SESSION_COOKIE_HTTPONLY=False,
    MAX_CONTENT_LENGTH=32 * 1024 * 1024,
    PREFERRED_URL_SCHEME=SCHEME,
    DEBUG=True
)
app.config.from_pyfile('config-extended.py')

socket_ = SocketIO(app, cors_allowed_origins="*")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = Scheduler()
mail = Mail(app)

services = [area.area, market.market, edu.edu]
for service in services:
    app.register_blueprint(service)

sockets = [area.socket, market.socket]
for socket in sockets:
    socket_ = socket.init_io(socket_)

Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.globals.update(url=url)
app.jinja_env.globals.update(game_role=get_game_roles)
db_session.global_init('db/database.sqlite')


def main():
    port = int(os.environ.get('PORT', 443))
    socket_.run(app, host='0.0.0.0', port=port, debug=True,
                keyfile='private.key', certfile='certificate.crt')


def add_admin_panel():
    admin_bp = Blueprint('admin-panel', __name__, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix="/admin")

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Переадресация страниц (используется в шаблонах)
    class MyAdminIndexView(AdminIndexView):
        @expose('/')
        def index(self):
            if not current_user.is_authenticated:
                return redirect(url_for('.login_page'))
            return super(MyAdminIndexView, self).index()

        @expose('/login/', methods=('GET', 'POST'))
        def login_page(self):
            if current_user.is_authenticated:
                return redirect(url_for('.index'))
            return super(MyAdminIndexView, self).index()

        @expose('/logout/')
        def logout_page(self):
            logout_user()
            return redirect(url_for('.index'))

        @expose('/reset/')
        def reset_page(self):
            return redirect(url_for('.index'))

    # Create admin
    admin = Admin(app, index_view=MyAdminIndexView(),
                  base_template='admin/master-extended.html')

    # Add view
    connect_models(admin)

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
            get_url=url_for
        )


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/secrets-of-literacy')
def secrets_of_literacy():
    return redirect('https://secrets-of-literacy.wixsite.com/website')


if __name__ == '__main__':
    add_admin_panel()
    main()
