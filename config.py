#  Nikulin Vasily © 2021
from flask_babel import _

HOST = 'area-146.tk'
DEV_HOST = 'area-146.ru'
SERVER_NAME = DEV_HOST
SCHEME = 'https' if SERVER_NAME == HOST else 'http'

default_constants = {
    'GOVERNMENT_BALANCE': 0,
    'FEE_FOR_STOCK': 0.001,
    'GAME_RUN': 0,
    'START_STOCKS': 100,
    'NEW_COMPANY_FEE': 500,
    'START_WALLET_MONEY': 1500,
    'MONTH_DURATION': 1,
    'MONTH_DURATION_UNIT': _('Дни'),
    'INCOME_TAX': 0.13,
    'PROPERTY_TAX': 0.02
}

sectors = sorted(list(map(lambda x: _(x),
                          [_('IT'), _('Энергетика'), _('Экономика'), _('Пищевая промышленность'),
                           _('Машиностроение'), _('Медицина'), _('Туризм'), _('Культура'),
                           _('Логистика')])))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'ico', 'webp'}

NEWS_PER_PAGE = 10

icons = {
    'new_company': 'business',
    'close_company': 'domain_disabled',
    'release_stocks': 'addchart',
    'new_post': 'post_add',
    'new_svoting': 'rule',
    'deal': 'published_with_changes',
    'investment': 'attach_money',
    'profit': 'attach_money',
    'property_tax': 'request_quote'
}
