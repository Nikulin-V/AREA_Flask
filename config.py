#  Nikulin Vasily © 2021
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

HOST = 'area-146.tk'
DEV_HOST = 'area-146.ru'
SCHEME = os.environ.get('SCHEME')
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True if os.environ.get('DEBUG').lower() in ['1', 'true', 't'] else False

SERVER_NAME = DEV_HOST if DEBUG else HOST
PORT = 443 if SCHEME == 'https' else 80

default_constants = {
    'GOVERNMENT_BALANCE': 0,
    'FEE_FOR_STOCK': 0.001,
    'GAME_RUN': 0,
    'START_STOCKS': 100,
    'NEW_COMPANY_FEE': 500,
    'START_WALLET_MONEY': 1500,
    'MONTH_DURATION': 1,
    'MONTH_DURATION_UNIT': 'Дни',
    'INCOME_TAX': 0.13,
    'PROPERTY_TAX': 0.02
}

sectors = sorted(
    ['IT', 'Энергетика', 'Экономика', 'Пищевая промышленность', 'Машиностроение',
     'Образование', 'Медицина', 'Туризм', 'Культура', 'Логистика']
)

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
