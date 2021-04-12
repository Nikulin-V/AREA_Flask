from flask import Flask, render_template, redirect, abort
from flask_login import logout_user, login_required, LoginManager, login_user, current_user
from flask_ngrok import run_with_ngrok

from data import db_session
from data.epos import EPOS
from data.users import User
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('C:/Users/Vasily/PycharmProjects/edu-area/db/database.sqlite')
epos = EPOS()

run_with_ngrok(app)


def main():
    app.run()


@app.route('/')
@app.route('/index')
@app.route('/main')
def index():
    if current_user.is_authenticated:
        return redirect('/homework')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        redirect('/homework')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user: User
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/homework")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect('/homework')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   btn_label='Войти')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   btn_label='Войти')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            email=form.email.data,
            epos_login=form.epos_login.data,
            epos_password=form.epos_password.data,
            school=form.school.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/profile')
    return render_template('register.html',
                           title='Регистрация',
                           form=form,
                           btn_label='Войти')


@app.route('/profile')
@login_required
def profile():
    form = RegisterForm()
    if form.validate_on_submit():
        user = current_user
        user.surname = form.surname.data
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.school = form.school.data
        user.role = form.role.data
        user.epos_login = form.epos_login.data
        user.date_of_birth = form.date_of_birth.data.date()
        user.about = form.about.data
        if form.epos_password.data:
            user.epos_password = form.epos_password.data
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   date=current_user.date_of_birth.date(),
                                   btn_label='Сохранить')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   date=current_user.date_of_birth.date(),
                                   btn_label='Сохранить')
        user = current_user
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/login')
    return render_template('profile.html',
                           title='Профиль',
                           form=form,
                           date=current_user.date_of_birth.date(),
                           btn_label='Сохранить')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/homework')
@login_required
def homework_page():
    if not current_user.is_authenticated:
        return abort(401)
    epos_login = current_user.epos_login
    epos_password = current_user.epos_password
    epos.run(epos_login, epos_password)
    schedule = epos.get_schedule()
    schedule: dict
    time_start = ['9:00', '9:55', '10:50', '11:55', '13:00', '13:55', '14:50', '15:45']
    time_end = ['9:45', '10:40', '11:35', '12:40', '13:45', '14:40', '15:35', '16:30']
    return render_template('homework.html', title='Дневник', schedule=schedule,
                           time_start=time_start, time_end=time_end)


@app.errorhandler(401)
@app.errorhandler(404)
def page_not_found(error):
    messages = {
        401: ['Вы не авторизованы',
              'Через несколько секунд Вы будете направлены на страницу авторизации'],
        404: ['Страница не найдена',
              'Проверьте правильность введённого адреса']
    }
    return render_template("error-page.html",
                           code=error.code,
                           title=messages[error.code][0],
                           message=messages[error.code][1])


if __name__ == '__main__':
    main()
