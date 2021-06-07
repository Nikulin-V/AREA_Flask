from datetime import date

from flask_mobility.decorators import mobile_template
from flask_mobility.mobility import Mobility
from flask import Flask, render_template, redirect, abort
from flask_login import logout_user, login_required, LoginManager, login_user, current_user
from flask_ngrok import run_with_ngrok

from data import db_session
from data.db_functions import repair_dependencies_students_and_groups
from data.epos import EPOS
from data.groups import Group
from data.homeworks import Homework
from data.projects_8_class import Project
from data.projects_8_class_offers import Offer
from data.projects_8_class_stocks import Stock
from data.projects_8_class_transactions import Transaction
from data.projects_8_class_votes import Vote
from data.schools import School
from data.students import Student
from data.users import User
from data.wallets import Wallet
from forms.login import LoginForm
from forms.profile import ProfileForm
from forms.purchase import PurchaseForm
from forms.register import RegisterForm
from forms.stocks import StocksForm
from forms.vote import VoteForm

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.me.readonly']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/database.sqlite')
epos = EPOS()

run_with_ngrok(app)


def main():
    app.run()


@app.route('/')
@app.route('/index')
@app.route('/main')
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template(template,
                           title='Главная')


@app.route('/login', methods=['GET', 'POST'])
@mobile_template('{mobile/}login.html')
def login(template):
    if current_user.is_authenticated:
        redirect('/profile')

    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user: User
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template(template,
                                   title='Авторизация',
                                   message="Вы не зарегистрированы в системе",
                                   form=form)
        if user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template(template,
                               title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template(template,
                           title='Авторизация',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
@mobile_template('{mobile/}register.html')
def register(template):
    if current_user.is_authenticated:
        redirect('/homework')

    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(template,
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   btn_label='Войти')

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(template,
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   btn_label='Войти')

        # noinspection PyArgumentList
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            patronymic=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            email=form.email.data,
            epos_login=form.epos_login.data,
            epos_password=form.epos_password.data,
            school_id=int(db_sess.query(School.id).
                          filter(School.title == form.school.data).first()[0]),
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/profile')

    return render_template(template,
                           title='Регистрация',
                           form=form,
                           btn_label='Войти')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
@mobile_template('{mobile/}profile.html')
def profile(template):
    form = ProfileForm()
    db_sess = db_session.create_session()
    user = current_user

    message = ''

    if form.validate_on_submit():
        message = "Сохранено"

        user.surname = form.surname.data
        user.name = form.name.data
        user.patronymic = form.patronymic.data
        user.email = form.email.data
        user.school_id = int(db_sess.query(School.id).filter(
            School.title == form.school.data).first()[0])
        user.role = form.role.data
        user.date_of_birth = form.date_of_birth.data
        user.about = form.about.data

        user.epos_login = form.epos_login.data
        if form.epos_password.data:
            user.epos_password = form.epos_password.data

        if form.old_password.data or form.password.data or form.password_again.data:
            if not form.old_password.data:
                message = "Введите старый пароль"
            elif not form.password.data:
                message = "Введите новый пароль"
            elif not form.password_again.data:
                message = "Повторите новый пароль"
            elif not user.check_password(form.old_password.data):
                message = "Неверный старый пароль"
            elif form.password.data != form.password_again.data:
                message = "Пароли не совпадают"
            else:
                user.set_password(form.password.data)

        db_sess.merge(user)
        db_sess.commit()

    return render_template(template,
                           title='Профиль',
                           form=form,
                           message=message,
                           school=db_sess.query(School.title).filter(
                               School.id == user.school_id).first()[0],
                           date=current_user.date_of_birth.strftime('%d.%m.%Y'),
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


@app.route('/area-diary')
@login_required
@mobile_template('{mobile/}area-diary.html')
def area_diary(template):
    repair_dependencies_students_and_groups()
    db_sess = db_session.create_session()
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']
    schedule = dict()
    for day in days:
        schedule[day] = [['-', -1] for _ in range(8)]

    # Получаем группы ученика и составляем по ним расписание
    group_ids = list(db_sess.query(Student.group_id).filter(Student.user_id == current_user.id))
    for group_id in group_ids:
        group = db_sess.query(Group).get(group_id)
        for day_n, lesson_n in list(map(lambda x: (int(x[0]), int(x[1])),
                                        str(group.schedule).split(','))):
            schedule[days[day_n - 1]][lesson_n - 1][0] = group.subject
            schedule[days[day_n - 1]][lesson_n - 1][1] = group_id[0]

    # Убираем пустые уроки с конца
    for key in schedule.keys():
        try:
            while schedule[key][-1][0] == '-':
                schedule[key] = schedule[key][:-1]
        except IndexError:
            pass

    begin_date = date(2021, 5, 3)
    homework = dict()
    for day in days:
        homework[day] = [[] for _ in range(8)]
    for day_n in range(6):
        for lesson_n in range(len(schedule[days[day_n - 1]])):
            homeworks = list(map(lambda x: str(x[0]).capitalize(),
                                 db_sess.query(Homework.homework).filter(
                                     Homework.date == date(begin_date.year,
                                                           begin_date.month,
                                                           begin_date.day + day_n),
                                     Homework.lesson_number == lesson_n,
                                     Homework.group_id == schedule[days[day_n]][lesson_n - 1][1]
                                 )))
            if homeworks:
                homework[days[day_n]][lesson_n - 1] = homeworks
    dates = [str(begin_date.day + i).rjust(2, '0') for i in range(6)]
    return render_template(template,
                           title='Дневник AREA',
                           schedule=schedule,
                           homework=homework,
                           dates=dates,
                           days=days)


@app.route('/epos-diary')
@login_required
@mobile_template('{mobile/}epos-diary.html')
def epos_diary(template):
    if not current_user.is_authenticated:
        abort(401)

    if not (current_user.epos_login and current_user.epos_password):
        abort(403)

    epos_login = current_user.epos_login
    epos_password = current_user.epos_password
    epos.run(epos_login, epos_password)
    response = epos.get_schedule()
    response: list
    schedule = []

    if response == 'bad password':
        abort(403)
    elif response == 'timeout':
        abort(408)
    else:
        schedule = response

    return render_template(template,
                           title='Дневник ЭПОСа',
                           schedule=schedule)


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(408)
@mobile_template('{mobile/}error-page.html')
def page_not_found(error, template):
    messages = {
        401: ['Вы не авторизованы',
              'Через несколько секунд Вы будете направлены на страницу авторизации'],
        403: ['Ошибка при авторизации в ЭПОС.Школа',
              'Попробуйте ещё раз. При повторном возникновении ошибки проверьте пароль от '
              'ЭПОС.Школа и обновите его в профиле'],
        404: ['Страница не найдена',
              'Проверьте правильность введённого адреса'],
        408: ['Превышено время ожидания',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку']
    }

    return render_template(template,
                           code=error.code,
                           title=messages[error.code][0],
                           message=messages[error.code][1])


@app.route('/privacy-policy')
@mobile_template('{mobile/}privacy-policy.html')
def privacy_policy(template):
    return render_template(template,
                           title='Политика конфиденциальности')


@app.route('/8-classes-projects-result', methods=['GET', 'POST'])
@mobile_template('{mobile/}8-classes-projects-result.html')
@login_required
def projects_8_class(template):
    db_sess = db_session.create_session()

    form = VoteForm()

    message = ''

    # self project
    # noinspection PyUnresolvedReferences
    project = db_sess.query(Project.id, Project.title). \
        filter(Project.authors_ids.contains(str(current_user.id))).first()
    points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                          filter(Vote.project_id == project[0]))))
    project = list(project) + [points]

    if form.is_submitted():
        if form.points.data is None:
            pass
        elif form.project.data == project[1]:
            message = 'Вы не можете голосовать за свой проект'
        elif 0 < form.points.data <= 100:
            project_id = db_sess.query(Project.id). \
                filter(Project.title == form.project.data).first()[0]
            current_voted_points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                                filter(Vote.user_id == current_user.id))))
            current_project_voted_points = db_sess.query(Vote.points). \
                filter(Vote.user_id == current_user.id,
                       Vote.project_id == project_id).first()
            if current_project_voted_points:
                current_project_voted_points = current_project_voted_points[0]
            else:
                current_project_voted_points = 0
            if current_voted_points + form.points.data <= 100 or \
                    current_project_voted_points >= form.points.data or \
                    (current_project_voted_points < form.points.data and
                     current_voted_points - current_project_voted_points + form.points.data <= 100):
                project_id = db_sess.query(Project.id). \
                    filter(Project.title == form.project.data).first()
                if project_id:
                    project_id = project_id[0]
                vote = db_sess.query(Vote).filter(Vote.user_id == current_user.id,
                                                  Vote.project_id == project_id).first()
                if vote:
                    vote.points = form.points.data
                    db_sess.merge(vote)
                else:
                    vote = Vote(user_id=current_user.id,
                                project_id=project_id,
                                points=form.points.data)
                    db_sess.add(vote)
                db_sess.commit()
            else:
                message = f'Вам не хватает очков.\n' \
                          f'Вы можете отменить голос, назначив проекту 0 очков.\n' \
                          f'Ваши очки: {100 - current_voted_points}/100'
        elif form.points.data == 0:
            project_id = db_sess.query(Project.id). \
                filter(Project.title == form.project.data).first()
            if project_id:
                project_id = project_id[0]
            vote = db_sess.query(Vote).filter(Vote.user_id == current_user.id,
                                              Vote.project_id == project_id).first()
            if vote:
                db_sess.delete(vote)
                db_sess.commit()
        else:
            message = 'Неверное число очков'

    sections, projects = evaluate_form(form)

    if not form.project.data:
        form.project.data = form.project.choices[0]
    project_id = db_sess.query(Project.id).filter(Project.title == form.project.data,
                                                  Project.section == form.section.data).first()
    if project_id:
        project_id = project_id[0]
    else:
        form.project.data = form.project.choices[0]
        project_id = db_sess.query(Project.id).filter(Project.title == form.project.data,
                                                      Project.section == form.section.data).first()
        if project_id:
            project_id = project_id[0]

    current_voted_points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                        filter(Vote.project_id == project_id,
                                               Vote.user_id == current_user.id))))

    form.points.data = current_voted_points if current_voted_points else 0

    return render_template(template,
                           form=form,
                           title='Проекты',
                           message=message,
                           project=project,
                           projects=projects,
                           sections=sections)


def evaluate_form(form):
    db_sess = db_session.create_session()
    projects = dict()
    sections = sorted(list(map(lambda x: x[0], set(list(db_sess.query(Project.section))))))

    # row structure: id | title | points | form
    for section in sections:
        data = list(db_sess.query(Project.id, Project.title).filter(Project.section == section))
        for row_id in range(len(data)):
            points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                  filter(Vote.project_id == data[row_id][0]))))
            data[row_id] = list(data[row_id]) + [points]
        projects[section] = sorted(data, key=lambda x: -x[2])

    form.section.choices = sorted(list(set(map(lambda x: x[0],
                                               list(db_sess.query(Project.section))))))

    if not form.section.data or form.section.data not in form.section.choices:
        form.section.errors = []
        form.section.data = form.section.choices[0]
    form.project.choices = list(map(lambda x: x[0],
                                    list(db_sess.query(Project.title).
                                         filter(Project.section == form.section.data))))

    users = list(map(lambda x: ' '.join(list(db_sess.query(User.surname, User.name).
                                        filter(User.id == x[0]).first())),
                     db_sess.query(Wallet.user_id)))

    if isinstance(form, StocksForm):
        form.user.choices = users
        if not users:
            form.user.data = None
        else:
            form.user.data = form.user.choices[0]

    return sections, projects


@app.route('/8-classes-market', methods=['GET', 'POST'])
@mobile_template('{mobile/}8-classes-market.html')
@login_required
def market_8_class(template):
    db_sess = db_session.create_session()

    form = StocksForm()
    purchase = PurchaseForm()

    evaluate_form(form)

    message = ''
    total = 0
    cheque = []

    money, stocks, market_stocks, offers = update_market_info()

    if purchase.accept.data:
        transactions = list(db_sess.query(Transaction).
                            filter(Transaction.user_id == current_user.id))
        for t in transactions:
            t: Transaction
            offer = db_sess.query(Offer).filter(Offer.id == t.offer_id).first()
            seller_id = offer.user_id
            customer_id = t.user_id

            seller_wallet = db_sess.query(Wallet).filter(Wallet.user_id == seller_id).first()
            customer_wallet = db_sess.query(Wallet).filter(Wallet.user_id == customer_id).first()
            stockholders_ids = list(set(db_sess.query(Stock.user_id, Stock.stocks).
                                        filter(Stock.project_id == offer.project_id,
                                               Stock.user_id != seller_id)))
            first_cost = t.stocks * t.price
            final_cost = first_cost + first_cost * (100 - t.stocks) * 0.001
            if customer_wallet.money >= final_cost:
                customer_stock = db_sess.query(Stock). \
                    filter(Stock.user_id == current_user.id,
                           Stock.project_id == offer.project_id).first()
                if offer.stocks > t.stocks:
                    offer.stocks -= t.stocks
                    offer.reserved_stocks -= t.stocks
                    db_sess.merge(offer)
                elif offer.stocks == t.stocks:
                    db_sess.delete(offer)
                if customer_stock:
                    customer_stock.stocks += t.stocks
                    db_sess.merge(customer_stock)
                else:
                    customer_stock = Stock(
                        user_id=current_user.id,
                        project_id=offer.project_id,
                        stocks=t.stocks
                    )
                    db_sess.add(customer_stock)
                db_sess.commit()
                customer_wallet.money -= final_cost
                seller_wallet.money += first_cost
                db_sess.merge(customer_wallet)
                db_sess.merge(seller_wallet)
                seller_stock = db_sess.query(Stock). \
                    filter(Stock.user_id == seller_id,
                           Stock.project_id == offer.project_id).first()
                if t.stocks < seller_stock.stocks:
                    seller_stock.stocks -= t.stocks
                for user_id, stocks in stockholders_ids:
                    wallet = db_sess.query(Wallet).filter(Wallet.user_id == user_id).first()
                    wallet.money += first_cost * stocks * 0.01
                    db_sess.merge(wallet)
                db_sess.delete(t)
                db_sess.commit()
            else:
                offer = db_sess.query(Offer).filter(Offer.id == t.offer_id).first()
                offer.reserved_stocks -= t.stocks
                db_sess.merge(offer)
                db_sess.delete(t)
                db_sess.commit()
                message = 'На балансе недостаточно средств'

    elif purchase.decline.data:
        transactions = list(db_sess.query(Transaction).
                            filter(Transaction.user_id == current_user.id))
        for t in transactions:
            offer = db_sess.query(Offer).filter(Offer.id == t.offer_id).first()
            offer.reserved_stocks -= t.stocks
            db_sess.delete(t)
            db_sess.commit()

    purchase = None
    if form.validate_on_submit() or (form.is_submitted() and form.action.data == 'Инвестировать'):
        if form.action.data == 'Инвестировать':
            if form.amount.data:
                investor_wallet = db_sess.query(Wallet).\
                    filter(Wallet.user_id == current_user.id).first()
                if investor_wallet.money >= form.amount.data:
                    surname, name = form.user.data.split()
                    user_id = db_sess.query(User.id).filter(User.surname == surname,
                                                            User.name == name)
                    wallet = db_sess.query(Wallet).filter(Wallet.user_id == user_id).first()
                    wallet.money += form.amount.data
                    investor_wallet.money -= form.amount.data
                    db_sess.merge(investor_wallet)
                    db_sess.merge(wallet)
                    db_sess.commit()
                    message = 'Инвестиция прошла успешно'
                else:
                    message = 'На балансе недостаточно средств'
        elif not form.stocks.data:
            pass
        elif form.action.data == 'Продать':
            project_id = get_project_id(form.project.data)
            project_stocks = list(filter(lambda x: x[0] == form.project.data, stocks))
            if project_stocks:
                project_stocks = project_stocks[0]
                if project_stocks[1] >= form.stocks.data:
                    if form.price.data >= 1:

                        offer = db_sess.query(Offer). \
                            filter(Offer.user_id == current_user.id,
                                   Offer.project_id == project_id,
                                   Offer.price == form.price.data).first()
                        if not offer:
                            offer = Offer(
                                user_id=current_user.id,
                                project_id=project_id,
                                stocks=form.stocks.data,
                                price=form.price.data
                            )
                            db_sess.add(offer)
                        else:
                            offer.stocks += form.stocks.data
                            db_sess.merge(offer)

                        stock = db_sess.query(Stock). \
                            filter(Stock.user_id == current_user.id,
                                   Stock.project_id == project_id).first()
                        if project_stocks[1] > form.stocks.data:
                            stock.stocks -= form.stocks.data
                            db_sess.merge(stock)
                        else:
                            db_sess.delete(stock)

                        db_sess.commit()

                        message = 'Акции выставлены на продажу'

                    else:
                        message = 'Неверная цена'
                else:
                    message = 'У Вас не хватает акций'
            else:
                message = 'У Вас нет акций этого проекта'
        elif form.action.data == 'Отменить продажу':
            project_id = get_project_id(form.project.data)
            market_project_stocks = list(filter(lambda x: x[0] == form.project.data,
                                                market_stocks))
            if market_project_stocks:
                market_project_stocks = list(filter(lambda x: x[3] == form.price.data,
                                                    market_project_stocks))
                if market_project_stocks:
                    market_project_stocks = market_project_stocks[0]
                    if market_project_stocks[1] - market_project_stocks[2] >= form.stocks.data:
                        user_offer = db_sess.query(Offer). \
                            filter(Offer.user_id == current_user.id,
                                   Offer.price == form.price.data).first()
                        user_stocks = db_sess.query(Stock). \
                            filter(Stock.user_id == current_user.id,
                                   Stock.project_id == project_id).first()
                        if not user_stocks:
                            user_stocks = Stock(
                                user_id=current_user.id,
                                project_id=project_id,
                                stocks=form.stocks.data
                            )
                            db_sess.add(user_stocks)
                        else:
                            user_stocks.stocks += form.stocks.data
                            db_sess.merge(user_stocks)

                        if market_project_stocks[1] > form.stocks.data or market_project_stocks[2]:
                            user_offer.stocks -= form.stocks.data
                            db_sess.merge(user_offer)
                        else:
                            db_sess.delete(user_offer)
                        db_sess.commit()

                        message = 'Акции сняты с торговой площадки'

                    else:
                        message = 'У Вас не хватает акций на торговой площадке. Также Вы не ' \
                                  'можете снять с продажи уже зарезервированные акции '
                else:
                    message = 'На торговой площадке нет Ваших акций данного проекта с указанной ' \
                              'ценой '
            else:
                message = 'На торговой площадке нет Ваших акций указанного проекта'
        elif form.action.data == 'Купить':
            market_offers = list(map(lambda x: (get_project_title(x[0]), x[1], x[2], x[3]),
                                     db_sess.query(Offer.project_id,
                                                   Offer.stocks,
                                                   Offer.reserved_stocks,
                                                   Offer.price).
                                     filter(Offer.project_id == get_project_id(form.project.data),
                                            Offer.user_id != current_user.id)))
            if market_offers:
                if sum(map(lambda x: x[1] - x[2], market_offers)) >= form.stocks.data:
                    purchase = PurchaseForm()
                    stocks_need = form.stocks.data
                    cheque = []
                    market_offers.sort(key=lambda x: x[-1])
                    while stocks_need:
                        available_stocks = market_offers[0][1] - market_offers[0][2]
                        if available_stocks and available_stocks <= stocks_need:
                            stocks_need -= available_stocks
                            offer = db_sess.query(Offer). \
                                filter(Offer.project_id == get_project_id(market_offers[0][0]),
                                       Offer.stocks == market_offers[0][1],
                                       Offer.reserved_stocks == market_offers[0][2]).first()
                            transaction = Transaction(
                                user_id=current_user.id,
                                offer_id=offer.id,
                                stocks=available_stocks,
                                price=offer.price
                            )
                            db_sess.add(transaction)
                            if not offer:
                                message = 'На торговой площадке нет в наличии такого ' \
                                          'количества акций указанного проекта'
                            else:
                                offer.reserved_stocks += available_stocks
                                cheque.append((get_project_title(offer.project_id),
                                               available_stocks,
                                               offer.price,
                                               available_stocks * offer.price))
                                db_sess.merge(offer)
                                db_sess.commit()
                        elif available_stocks and available_stocks > stocks_need:
                            offer = db_sess.query(Offer). \
                                filter(Offer.project_id == get_project_id(market_offers[0][0]),
                                       Offer.stocks == market_offers[0][1],
                                       Offer.reserved_stocks == market_offers[0][2]).first()
                            transaction = Transaction(
                                user_id=current_user.id,
                                offer_id=offer.id,
                                stocks=stocks_need,
                                price=offer.price
                            )
                            db_sess.add(transaction)
                            if not offer:
                                message = 'На торговой площадке нет в наличии такого ' \
                                          'количества акций указанного проекта'
                            else:
                                offer.reserved_stocks += stocks_need
                                cheque.append((get_project_title(offer.project_id),
                                               stocks_need,
                                               offer.price,
                                               stocks_need * offer.price))

                                stocks_need = 0
                                db_sess.merge(offer)
                                db_sess.commit()
                        market_offers.pop(0)

                    total = sum(map(lambda x: x[-1], cheque))
                    cheque.append(('Комиссия', '-', '-',
                                   (100 - sum(map(lambda x: x[1], cheque))) * total * 0.001))

                else:
                    message = 'На торговой площадке нет в наличии такого количества акций ' \
                              'указанного проекта '
            else:
                message = 'На торговой площадке нет акций указанного проекта'

    money, stocks, market_stocks, offers = update_market_info()

    market_stocks = sorted(market_stocks, key=lambda x: x[-1])
    offers = sorted(offers, key=lambda x: x[-1])

    return render_template(template,
                           form=form,
                           title='Торговая площадка',
                           message=message,
                           money=money,
                           stocks=stocks,
                           market_stocks=market_stocks,
                           offers=offers,
                           purchase=purchase,
                           cheque=cheque,
                           total=total)


def get_project_title(identifier):
    return db_session.create_session().query(Project.title). \
        filter(Project.id == identifier).first()[0]


def get_project_id(title):
    return db_session.create_session().query(Project.id). \
        filter(Project.title == title).first()[0]


def update_market_info():
    db_sess = db_session.create_session()
    # Получаем акции пользователя
    # title | stocks
    stocks = list(map(lambda x: (get_project_title(x[0]), x[1]),
                      db_sess.query(Stock.project_id, Stock.stocks).
                      filter(Stock.user_id == current_user.id)))

    # Получаем акции пользователя на торговой площадке
    # title | stocks | reserved_stocks | price
    market_stocks = list(map(lambda x: (get_project_title(x[0]), x[1], x[2], x[3]),
                             db_sess.query(Offer.project_id, Offer.stocks,
                                           Offer.reserved_stocks, Offer.price).
                             filter(Offer.user_id == current_user.id)))

    # Получаем текущие предложения на рынке
    # title | stocks | reserved_stocks | price
    offers = list(map(lambda x: (get_project_title(x[0]), x[1], x[2], x[3]),
                      db_sess.query(Offer.project_id, Offer.stocks,
                                    Offer.reserved_stocks, Offer.price)))

    # Получаем баланс кошелька
    money = db_sess.query(Wallet.money).filter(Wallet.user_id == current_user.id).first()
    if not money:
        default = 1000
        if 'Эксперт' in current_user.role:
            default = 10000
        wallet = Wallet(
            user_id=current_user.id,
            money=default
        )
        db_sess.add(wallet)
        db_sess.commit()
        money = default
    else:
        money = round(money[0], 2)

    return money, stocks, market_stocks, offers


if __name__ == '__main__':
    main()
