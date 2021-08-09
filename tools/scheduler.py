#  Nikulin Vasily © 2021

import datetime
from threading import Thread

from data import db_session
from data.companies import Company
from data.offers import Offer
from data.scheduled_job import ScheduledJob
from data.stockholders_votes import SVote

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
        self.db_sess = db_session.create_session()

    def delete_model(self):
        model = self.db_sess.query(models[self.job.model]).get(str(self.job.object_id))
        if model is None:
            return False
        self.db_sess.delete(model)
        self.db_sess.commit()
        return True

    def undo_buying(self):
        count = int(self.job.action.split()[1])
        model = self.db_sess.query(models[self.job.model]).get(str(self.job.object_id))
        if model is None:
            return False
        model.reserved_stocks -= count
        if model.reserved_stocks < 0:
            model.reserved_stocks = 0
        self.db_sess.merge(model)
        self.db_sess.commit()
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

        log = f'{datetime.datetime.now()}\t|\t{result}\t|\t' \
              f'{action}\t|\t{model}\t|\t{object_id}\n'
        f = open('logs.txt', 'a')
        f.write(log)
        f.close()


scheduler = Scheduler()
