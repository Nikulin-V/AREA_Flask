#  Nikulin Vasily © 2021
from flask import Blueprint
from flask_cors import CORS

from tools.io_blueprint import IOBlueprint

api = Blueprint('api', __name__)
socket = IOBlueprint()

CORS(api)

from .companies import createCompany, getCompanies, deleteCompany
from .news import createNews, getNews, editNews, deleteNews, uploadImage
from .offers import createOffer, getOffers, editOffer, deleteOffer
from .sessions import createSession, getSessions, editSession, deleteSession
from .stocks import getStocks
from .svotes import createStockholdersVoting, getStockholdersVotes, voteInStockholdersVoting
from .votes import getCompaniesVotes, voteInCompaniesVoting
from .wallets import getWalletMoney, getWallets
