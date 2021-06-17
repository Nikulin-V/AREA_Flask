from flask import Flask
from flask_login import LoginManager
from flask_mobility.mobility import Mobility

from data import db_session
from data.users import User
from site_pages import pages_blueprints

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.me.readonly']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

for blueprint in pages_blueprints:
    app.register_blueprint(blueprint)

Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/database.sqlite')


def main():
    app.run(host='0.0.0.0', port=80)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
