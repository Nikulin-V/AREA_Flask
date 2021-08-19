#  Nikulin Vasily © 2021
import datetime

from flask import render_template, abort
from flask_login import login_required

from data import db_session
from data.config import Constant
from data.functions import get_game_roles, get_session_id, get_constant
from data.scheduled_job import ScheduledJob
from forms.config_management import ConfigManagementForm
from market import market


@market.route('/game-panel', methods=['GET', 'POST'])
@login_required
def game_panel():
    if 'Admin' not in get_game_roles():
        abort(403)

    db_sess = db_session.create_session()

    form = ConfigManagementForm()
    message = ''

    if form.validate_on_submit():
        game_run = db_sess.query(Constant).filter(
            Constant.name == 'GAME_RUN',
            Constant.session_id == get_session_id()
        ).first()
        if game_run.value == 0 and form.game_run.data:
            start_working_time()
        game_run.value = 1 if form.game_run.data else 0
        db_sess.merge(game_run)

        constants = [
            ('GAME_RUN', form.game_run.data),
            ('START_WALLET_MONEY', form.start_wallet_money.data),
            ('FEE_FOR_STOCK', form.fee.data),
            ('NEW_COMPANY_FEE', form.new_company_fee.data),
            ('START_STOCKS', form.start_stocks.data),
            ('MONTH_DURATION', form.month_duration.data),
            ('MONTH_DURATION_UNIT', form.month_duration_unit.data),
            ('PROPERTY_TAX', form.property_tax.data),
            ('INCOME_TAX', form.income_tax.data)
        ]

        for constant_name, form_field_data in constants[1:]:
            if form_field_data:
                constant = db_sess.query(Constant).filter(
                    Constant.name == constant_name,
                    Constant.session_id == get_session_id()).first()
                constant.value = form_field_data
                db_sess.merge(constant)

        db_sess.commit()
        message = 'Сохранено'

    form.game_run.data = get_constant('GAME_RUN')

    if not form.start_wallet_money.data:
        form.start_wallet_money.data = get_constant('START_WALLET_MONEY')

    if not form.fee.data:
        form.fee.data = get_constant('FEE_FOR_STOCK')

    if not form.new_company_fee.data:
        form.new_company_fee.data = get_constant('NEW_COMPANY_FEE')

    if not form.start_stocks.data:
        form.start_stocks.data = get_constant('START_STOCKS')

    if not form.month_duration.data:
        form.month_duration.data = get_constant('MONTH_DURATION')

    if not form.month_duration_unit.data:
        form.month_duration_unit.data = get_constant('MONTH_DURATION_UNIT')

    if not form.property_tax.data and form.property_tax.data != 0:
        form.property_tax.data = get_constant('PROPERTY_TAX')

    if not form.income_tax.data and form.income_tax.data != 0:
        form.income_tax.data = get_constant('INCOME_TAX')

    return render_template("market/session_panel.html",
                           title='Управление фондовой биржей',
                           message=message,
                           form=form)


# TODO: Перевести


def start_working_time():
    db_sess = db_session.create_session()

    start_property_taxing(db_sess)
    start_making_profit(db_sess)


def start_making_profit(db_sess, session_id=None):
    if session_id is None:
        session_id = get_session_id()
    making_profit_date = db_sess.query(ScheduledJob).filter(
        ScheduledJob.model == 'Session',
        ScheduledJob.action == 'Making profit',
        ScheduledJob.id == session_id
    ).first()

    if making_profit_date and making_profit_date.datetime < datetime.datetime.now():
        db_sess.delete(making_profit_date)
        db_sess.commit()
        making_profit_date = None

    if making_profit_date is None:
        making_profit_date = ScheduledJob(
            model='Session',
            object_id=session_id,
            action='Making profit',
            datetime=datetime.datetime.now() + get_month_duration(session_id)
        )
        db_sess.add(making_profit_date)
        db_sess.commit()


def start_property_taxing(db_sess, session_id=None):
    if session_id is None:
        session_id = get_session_id()
    property_taxing_date = db_sess.query(ScheduledJob).filter(
        ScheduledJob.model == 'Session',
        ScheduledJob.action == 'Property taxing',
        ScheduledJob.id == session_id,
    ).first()

    if property_taxing_date and property_taxing_date.datetime < datetime.datetime.now():
        db_sess.delete(property_taxing_date)
        db_sess.commit()
        property_taxing_date = None

    if property_taxing_date is None:
        property_taxing_date = ScheduledJob(
            model='Session',
            object_id=session_id,
            action='Property taxing',
            datetime=datetime.datetime.now() + 3 * get_month_duration(session_id)
        )
        db_sess.add(property_taxing_date)
        db_sess.commit()


def get_month_duration(session_id):
    month_duration_unit = get_constant('MONTH_DURATION_UNIT', session_id)
    month_duration_value = get_constant('MONTH_DURATION', session_id)
    if month_duration_unit == 'Дни':
        return datetime.timedelta(days=month_duration_value)
    elif month_duration_unit == 'Часы':
        return datetime.timedelta(hours=month_duration_value)
    elif month_duration_unit == 'Минуты':
        return datetime.timedelta(minutes=month_duration_value)
    return datetime.timedelta(seconds=month_duration_value)
