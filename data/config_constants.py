from data import db_session
from data.config import Constant


def get_constant(name):
    db_session.global_init('db/database.sqlite')
    db_sess = db_session.create_session()
    constant = db_sess.query(Constant.value).filter(Constant.name == name).first()
    if constant:
        constant = constant[0]
    return constant


PROFIT_PERCENT = get_constant('PROFIT_PERCENT')
GAME_RUN = get_constant('GAME_RUN')
