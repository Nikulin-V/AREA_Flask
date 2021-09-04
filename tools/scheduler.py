#  Nikulin Vasily © 2021
import datetime
from threading import Thread

from config import sectors
from data import db_session
from data.companies import Company
from data.config import Constant
from data.functions import get_constant
from data.offers import Offer
from data.scheduled_job import ScheduledJob
from data.sessions import Session
from data.stockholders_votes import SVote
from data.stocks import Stock
from data.votes import Vote
from data.wallets import Wallet
from market.api.companies import delete_all_company_data
from tools.tools import safe_remove, is_stockholder

models = {
    'SVote': SVote,
    'Company': Company,
    'Offer': Offer
}


class Scheduler(Thread):
    def __init__(self):
        super().__init__()
        self.works = False

    def run(self):
        self.works = True
        db_sess = db_session.create_session()
        for j in db_sess.query(ScheduledJob).all():
            j: ScheduledJob
            if (datetime.datetime.now() - j.datetime) > datetime.timedelta():
                db_sess.delete(j)
                db_sess.commit()
                Task(j).start()
        self.works = False


class Task(Thread):
    def __init__(self, job):
        Thread.__init__(self)
        self.job = job

    def delete_model(self):
        db_sess = db_session.create_session()
        model = db_sess.query(models[self.job.model]).get(str(self.job.object_id))
        if model is None:
            return False
        db_sess.delete(model)
        db_sess.commit()
        return True

    def undo_buying(self):
        db_sess = db_session.create_session()
        count = int(self.job.action.split()[1])
        model = db_sess.query(models[self.job.model]).get(str(self.job.object_id))
        if model is None:
            return False
        model.reserved_stocks -= count
        if model.reserved_stocks < 0:
            model.reserved_stocks = 0
        db_sess.merge(model)
        db_sess.commit()
        return True

    def delete_unused_picture(self):
        path = self.job.object_id
        return safe_remove(path)

    def property_taxing(self):
        db_sess = db_session.create_session()
        session_id = self.job.object_id

        property_tax_percent = float(get_constant('PROPERTY_TAX', session_id))

        wallets = db_sess.query(Wallet).filter(Wallet.session_id == session_id).all()

        government_balance = db_sess.query(Constant).filter(
            Constant.session_id == session_id,
            Constant.name == 'GOVERNMENT_BALANCE'
        ).first()
        government_balance.value = float(government_balance.value)

        for wallet in wallets:
            property_tax = wallet.money * property_tax_percent
            wallet.money -= property_tax
            government_balance.value += property_tax
            db_sess.merge(wallet)
            db_sess.merge(government_balance)
        #     Рассылка уведомлений
        #     now = datetime.datetime.now()
        #     lazy_messages.append((
        #         wallet.user_id,
        #         {
        #             'message': 'Success',
        #             'notifications': [
        #                 {
        #                     'logoSource': icons['new_svoting'],
        #                     'header_up': f'-{property_tax}'
        #                                  f'<span class="material-icons-round md-money">'
        #                                  f'paid</span>',
        #                     'header_down': 'Налог на имущество',
        #                     'date': now.strftime('%d %B'),
        #                     'time': now.strftime('%H:%M'),
        #                 }
        #             ],
        #             'errors': []
        #         })
        #     )

        db_sess.commit()
        return True

    def making_profit(self):
        db_sess = db_session.create_session()

        session_id = self.job.object_id
        companies_votes = \
            dict(
                (sector, dict(
                    (company.id, 0)
                    for company in db_sess.query(Company).filter(
                        Company.session_id == session_id,
                        Company.sector == sector
                    ).all()
                ))
                for sector in sectors)

        for user_id in db_sess.query(Session).get(session_id).players_ids.split(';'):
            for sector in sectors:
                sector_companies = list(filter(
                    lambda x: is_stockholder(x, user_id, session_id), companies_votes[sector].keys()
                ))

                points = 100
                # Распределение очков
                for vote in db_sess.query(Vote).filter(
                        Vote.session_id == session_id,
                        Vote.user_id == user_id
                ).all():
                    if vote.company_id in sector_companies:
                        companies_votes[vote.sector][vote.company_id] += vote.points
                        points -= vote.points
                # Распределение оставшихся очков для сектора между компаниями
                if points and len(sector_companies) != 0:
                    points_per_company = points / len(sector_companies)
                    for company_id in sector_companies:
                        companies_votes[sector][company_id] += points_per_company

        filled_sectors = []
        for sector in sectors:
            if len(companies_votes[sector].keys()) > 0:
                filled_sectors.append(sector)
        if not filled_sectors:
            return False

        government_balance = db_sess.query(Constant).filter(
            Constant.session_id == session_id,
            Constant.name == 'GOVERNMENT_BALANCE'
        ).first()
        government_balance.value = float(government_balance.value)
        income_tax_percent = float(get_constant('INCOME_TAX', session_id))
        income_tax = government_balance.value * income_tax_percent
        db_sess.merge(government_balance)
        profit = government_balance.value - income_tax
        government_balance.value = income_tax
        profit_per_sector = profit / len(filled_sectors)

        # stockholders = dict()

        for sector in filled_sectors:
            profit_per_company = profit_per_sector / len(companies_votes[sector].keys())
            for company_id in companies_votes[sector]:
                all_stocks_count = sum(map(lambda x: x[0], db_sess.query(Stock.stocks).filter(
                    Stock.session_id == session_id,
                    Stock.company_id == company_id
                ).all())) + sum(map(lambda x: x[0], db_sess.query(Offer.stocks).filter(
                    Offer.session_id == session_id,
                    Offer.company_id == company_id
                ).all()))
                all_stocks = list(db_sess.query(Stock).filter(
                    Stock.session_id == session_id,
                    Stock.company_id == company_id
                ).all()) + list(db_sess.query(Offer).filter(
                    Offer.session_id == session_id,
                    Offer.company_id == company_id
                ).all())
                if all_stocks_count == 0:
                    ghost_company = db_sess.query(Company).get(company_id)
                    delete_all_company_data(company_id)
                    db_sess.delete(ghost_company)
                    continue

                profit_per_stock = profit_per_company / all_stocks_count
                for stock in all_stocks:
                    wallet = db_sess.query(Wallet).filter(
                        Wallet.user_id == stock.user_id
                    ).first()
                    wallet.money += profit_per_stock * stock.stocks
                    db_sess.merge(wallet)
                    # if stock.user_id in stockholders.keys():
                    #     stockholders[stock.user_id] += profit_per_stock * stock.stocks
                    # else:
                    #     stockholders[stock.user_id] = profit_per_stock * stock.stocks
        # Рассылка уведомлений
        # for stockholder_id, profit in stockholders.items():
        #     now = datetime.datetime.now()
        #     lazy_messages.append((
        #         stockholder_id,
        #         {
        #             'message': 'Success',
        #             'notifications': [
        #                 {
        #                     'logoSource': icons['profit'],
        #                     'header_up': f'+{profit}'
        #                                  f'<span class="material-icons-round md-money">'
        #                                  f'paid</span>',
        #                     'header_down': 'Дивиденды с акций',
        #                     'date': now.strftime('%d %B'),
        #                     'time': now.strftime('%H:%M'),
        #                 }
        #             ],
        #             'errors': []
        #         }
        #     )
        #     )

        db_sess.commit()
        return True

    def run(self):
        result = 'Success'
        action = self.job.action
        model = self.job.model
        object_id = self.job.object_id
        if action == 'Delete':
            if not self.delete_model():
                result = 'Failed'
        elif action.startswith('Undo'):
            if not self.undo_buying():
                result = 'Failed'
        elif action == 'Delete unused picture':
            if not self.delete_unused_picture():
                result = 'Failed'
        elif action == 'Property taxing' and int(get_constant('GAME_RUN', self.job.object_id)) == 1:
            if not self.property_taxing():
                result = 'Failed'
            from market.game_panel import start_property_taxing
            db_sess = db_session.create_session()
            start_property_taxing(db_sess, self.job.object_id)
        elif action == 'Making profit' and int(get_constant('GAME_RUN', self.job.object_id)) == 1:
            if not self.making_profit():
                result = 'Failed'
            from market.game_panel import start_making_profit
            db_sess = db_session.create_session()
            start_making_profit(db_sess, self.job.object_id)
        log = f'{datetime.datetime.now()}\t|\t{result.ljust(7, " ")}\t|\t' \
              f'{action.ljust(21, " ")}\t|\t{model.ljust(20, " ")}\t|\t{object_id}\n'
        f = open('logs.txt', 'a')
        f.write(log)
        f.close()
