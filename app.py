from flask import Flask, render_template, redirect
from flask_login import logout_user, login_required, LoginManager

from data import db_session
from data.users import User
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    app.run(debug=True)


@app.route('/')
@app.route('/index')
@app.route('/main')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.name.data,
            name=form.name.data,
            last_name=form.name.data,
            date_of_birth=form.name.data,
            school=form.name.data,
            email=form.name.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/homework')
def homework_page():
    table = []
    homework = [
        ['Информатика', 'Физика', 'Геометрия', '', '', '', ''],
        ['Английский язык', 'Физика', 'Литература', '', '', '', ''],
        ['Информатика', 'Алгебра', 'Литература', '', '', '', ''],
        ['Биология', 'Алгебра', 'Химия', '', '', '', ''],
        ['Физика', 'История', 'ОБЖ', '', '', '', ''],
        ['Физика', 'Английский язык', 'Английский язык', '', '', '', ''],
        ['Обществознание', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '']
    ]
    time_start = ['9:00', '9:55', '10:50', '11:55', '13:00', '13:55', '14:50', '15:45']
    time_end = ['9:45', '10:40', '11:35', '12:40', '13:45', '14:40', '15:35', '16:30']
    for lesson_id in range(8):
        table.append([f'{time_start[lesson_id]} - {time_end[lesson_id]}',
                      *[homework[lesson_id][day_id] for day_id in range(7)]])
    return render_template('homework.html', table=table)


if __name__ == '__main__':
    main()
